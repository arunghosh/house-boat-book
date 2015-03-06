
app.controller('searchCtrl', function($scope, $cookieStore, $location, priceApi, searchApi, listApi, boatsApi){

	$scope.showPolicy = function(boat){
		boatsApi.datePolicy(boat, $scope.order.date).success(function (policies){
			$scope.policies = policies;
		});
	}

	$scope.showReview = function(boat){
		boatsApi.reviews(boat.id).success(function (reviews){
			$scope.reviews = reviews;
		});
	}	

	$scope.toggleDetails = function(b){
		b._images = b._images ? null : b.images;
	}

	$scope.toggleFilter = function(item){
		$scope.showBusy = true;
		item.checked = item.checked ? !item.checked : true;
		
		var query = {};
		$scope.filters.map(function(f){
			query[f.name] = f._values.reduce(function(a,b){
				if(b.checked === true) a.push(b.id);
				return a;
			},[]);;
		});

		searchApi.boatIds(query).success(function(ids){
			$scope.boats.map(function(b){
				b.hide = !ids.contains(b.id);
			});
			refreshTotal();
			$scope.showBusy = false;
		});
	};

	$scope.showFilter = function(f){
		$scope.filters.map(function(fi){
			fi.values = [];
		});
		f.values = f._values;
	};

	$scope.showBook = function(boat){
		$cookieStore.put('order', $scope.order);
		$cookieStore.put('boat', boat);
		$location.path('book');
	};

	$scope.$watch("order.no_adult", refreshTotal);
	$scope.$watch("order.no_child", refreshTotal);
	$scope.$watch("order.date", function(newDate, oldDate){
		if(newDate != oldDate && newDate && $scope.boats){
			onDateChange();
		}
	});

	function onDateChange(){
		$scope.showBusy = true;
		boatsApi.booked($scope.order.date).success(function(result){
			$scope.boats.map(function(b){
				b.isBooked = result.contains(b.id);
			});
		});
		priceApi.byDate($scope.order.date).success(function(result){
			result.map(function(p){
				$scope.boats.getById(p.boat_id).price = p;
			});
			refreshTotal();
			$scope.showBusy = false;
		});
	}

	function refreshTotal(){
		$scope.boats.map(function(b){
			if(b.price){
				var order = $scope.order;
				var total = Number(b.price.base) + order.no_child * b.price.child;
				total += (order.no_adult > b.no_adult) ? (order.no_adult - b.no_adult) * b.price.adult : 0;
				b.price.total = total;
				b.overload = (b.max_adult < order.no_adult) || (b.max_child < order.no_child);
			}
		});
	}

	// function fillFilters(){
	// 	var amenities = $scope.boats.reduce(function(a,b){
	// 		return a.concat(b.amenities.reduce(function(o,i){
	// 			if(!a.contains(i) && !o.contains(i)) o.push(i);
	// 			return o;
	// 		},[])).sort();
	// 	}, []);
	// 	var acTypes = $scope.boats.map(function(b){return b.ac_type;}).distinct();
	// 	debugger;
	// }

	function init(){
		$scope.showBusy = false;
		$scope.filters = $scope.boats = [];
		boatsApi.active().success(function(boats){
			$scope.boats = boats;
			onDateChange();
		});

	    listApi.amenities().success(function(amenities){
	    	initFilter(amenities);
	    	$scope.filters.push({name:"amenities", _values:amenities, values:[]})
	    });

	    listApi.acTypes().success(function(acTypes){
	    	initFilter(acTypes);
	        $scope.filters.push({name:"AC", _values:acTypes, values:[]})
	    });

	    initOrder();

		function initFilter(filters){
	    	filters.map(function(a){
	    		a.checked = false;
	    	});
		}
	
		function initOrder(){
			if($cookieStore.get('order')){
		    	$scope.order = $cookieStore.get('order');
		    	$scope.order.date = new Date($scope.order.date);
		    	$scope.order.no_child = $scope.order.no_child ? $scope.order.no_child : 0;
		    	$scope.order.no_adult = $scope.order.no_adult ? $scope.order.no_adult : 2;
			} else {	
				$location.path('/');
			}
		}
	}

	init();

});
