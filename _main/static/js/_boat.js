app.config(function($routeProvider){
    $routeProvider
    .when('/price',
    {
        templateUrl:common.getHtmlUrl('boat/price'),
        controller:'priceCtrl'
    })
    .when('/mtnc',
    {
        templateUrl:common.getHtmlUrl('boat/mtnc'),
        controller:'mtncCtrl'
    })
    .when('/amty',
    {
        templateUrl:common.getHtmlUrl('boat/amenity'),
        controller:'amtyCtrl'
    })
    .when('/reviews',
    {
        templateUrl:common.getHtmlUrl('boat/review'),
        controller:'reviewCtrl'
    })
    .when('/calendar',
    {
        templateUrl:common.getHtmlUrl('boat/calendar'),
        controller:'calendarCtrl'
    })
    .when('/cpolicy',
    {
        templateUrl:common.getHtmlUrl('bok/cpolicy'),
        controller:'cpolicyCtrl'
    })
    .when('/',
    {
        templateUrl:common.getHtmlUrl('boat/overview'),
        // controller:'overviewCtrl'
    })
    .when('/orders',
    {
        templateUrl:common.getHtmlUrl('boat/orders'),
        controller:'orderCtrl'
    });
});


app.controller('boatCtrl', function($scope, $location, $controller, listApi, boatsApi){
	$controller('baseDbCtrl', {$scope: $scope}); 
	var boatId = $scope.urlId;

	function init(){
		boatsApi.details(boatId).success(function(boat){
			$scope.boat = boat;
		});	

	    listApi.acTypes().success(function(acTypes){
	        $scope.acTypes = acTypes;
	    });
		$scope.refreshSelection();
	}

	$scope.showEdit = function(){
		$scope.nBoat = angular.copy($scope.boat);
	};

    $scope.update = function(){
	    boatsApi.update($scope.nBoat).success(function(boat){
	    	$scope.boat = boat;
	    	$scope.nBoat = null;
        }).error(function(){
        	alert("Update Failed. Contact Admin.");
        });
    };

	$scope.routes = [
		{ name:"Overview", url:"", icon:"dashboard" },	
		{ name:"Calendar", url:"calendar", icon:"calendar" },	
		{ name:"Orders", url:"orders", icon:"bookmark" },
		{ name:"Pricing", url:"price", icon:"usd" },
		{ name:"Cancel Policy", url:"cpolicy", icon:"ban-circle" },
		{ name:"Maintanence", url:"mtnc", icon:"wrench" },
		{ name:"Amenities", url:"amty", icon:"briefcase" },
		{ name:"User Reviews", url:"reviews", icon:"star" },
		{ name:"Photos", url:"photos", icon:"picture" },
	];

	init();
});


app.controller('reviewCtrl', function($scope, $controller, $location, boatsApi){
	$controller('baseDbCtrl', {$scope: $scope}); 
	var rc = {};
	boatsApi.reviews($scope.urlId).success(function(reviews){
		rc.reviews = reviews;
	})
	$scope.rc = rc;
});


app.controller('orderCtrl', function($scope, $controller, $location, boatsApi){
	$controller('baseDbCtrl', {$scope: $scope}); 
	var boatId = $scope.urlId;
	var oc = {boatId:boatId};
	boatsApi.orders(boatId).success(function(orders){
		oc.orders = orders;
	})
	$scope.oc = oc;
});

app.controller('calendarCtrl', function($scope, $controller, $location, priceApi){
	$controller('baseDbCtrl', {$scope: $scope}); 
	var boatId = $scope.urlId;
	var cc = { weekDays: common.weekDays, boatId:boatId, createView:null };

	cc.getOrCreate = function(d){
		if(d.order_id > -1){
			cc.orderId = d.order_id;
		} else {
			cc.date = d.date;
			cc.createView = true;
		}
	};

	cc.set = function(yymm){
		cc.yymm = yymm;
		var yyyy = Math.floor(yymm / 12);
		var mm = (yymm % 12) + 1;
		priceApi.month(boatId, yyyy, mm).success(function(result){
			var top = 0;
			var month = {
				name: common.monthNames[mm - 1],
				year: yyyy, 
				days: [],
				monthInt: month
			};
			result.data.map(function(d){
				var date = new Date(d.date);
				d.day = date.getDate();
				d.delta = d.price - result.price;
				d.wday = date.getDay();
				if(month.blanks === undefined){
					month.blanks = new Array(d.wday);
				}
				month.days.push(d);
			});
			cc.month = month;
		});
	}
	var date = new Date();
	cc.set((date.getFullYear() * 12) + date.getMonth());
	$scope.cc = cc;
});

app.controller('amtyCtrl', function($scope, boatsApi, listApi, $controller){
	$controller('baseDbCtrl', {$scope: $scope}); 
	var boatId = $scope.urlId;
	var amc = {};

	boatsApi.details(boatId).success(function(boat){
		amc.boat = boat;
		listApi.amenities().success(function(amenities){
			amenities.map(function(a){
				a.checked = boat.amenities.contains(a.name);
				a.toggle = function(){
					boatsApi.updateAmenities({
						boat_id: boat.id,
						amenity_id: a.id,
						status: a.checked ? 0 : 1})
					.success(function(){
						a.checked = !a.checked;
						if(a.checked) boat.amenities.push(a.name);
						else boat.amenities.remove(a.name);})
					.error(function(){
						alert("Failed to update amenities. Contact Admin.");
					});
				};
			});
			amc.amenities = amenities;
		});
	});	

	$scope.amc = amc;
});

app.controller('mtncCtrl', function($scope, boatsApi, $routeParams, $controller){
	$controller('baseDbCtrl', {$scope: $scope}); 
	var boatId = $scope.urlId;
	var mc = {};

	boatsApi.mtncs(boatId).success(function(mtncs){
		mc.mtncs = mtncs;
	})

	mc.edit = function(mtnc){
		if(mtnc === undefined){
			mtnc = {
				date_from: new Date(),
				date_to: new Date()
			};
		}
		mc.mtnc = mtnc;
		mc.error = null;
	};

	mc.update = function(){
		boatsApi.updateMtnc(mc.mtnc, boatId).success(function(result){
			if(result.status == true) {
				mc.mtncs.remove(mc.mtnc);
				mc.mtncs.push(result.data);
				mc.mtnc = null;
			} else {
				mc.error = result.msg;	
			}
		})
	};

	$scope.mc = mc;
});


app.controller('priceCtrl', function($scope, priceApi, $routeParams, $controller){
	$controller('baseDbCtrl', {$scope: $scope}); 
	var boatId = $scope.urlId;
	var pc = {};

	priceApi.forBoat(boatId).success(function(prices){
		pc.season = prices.season;
		pc.base = prices.base;
	});	

	pc.update = function(){
		if(pc.price === pc.base) updateBase();
		else updateSeason();
	}

	function updateBase(){
		pc.base.boat_id = boatId;
		priceApi.updateBase(pc.base).success(function(result){
			if(result.status == true) {
				pc.base = result.data;
				pc.price = null;
			} else {
				pc.error = result.msg;	
			}
		}).error(function(msg){
			pc.error = "Failed to update price";
		});
	}

	function updateSeason(){
		pc.price.boat_id = boatId;
		var price = pc.price;
		if(price.date_from == null || price.date_to == null){
			price.error = "Dates cannot be empty. Enter from and to date";
			return;
		}
		priceApi.updateSeason(price).success(function(result){
			if(result.status == true) {
				pc.season.remove(price);
				result.data.isUpdated = true;
				pc.season.push(result.data);
				pc.price = null;
			} else {
				pc.error = result.msg;	
			}
		}).error(function(msg){
			pc.error = "Failed to update price";
		});
	}

	pc.edit = function(price){
		if(price === undefined){
			price = angular.copy(pc.base);
			price.id = null;
			price.date_from = new Date();
			price.date_to = new Date();
		}
		pc.price = price;
		pc.error = null;
	};

	$scope.pc = pc;
});


app.directive('boatEdit',['boatsApi', 'listApi', function(boatsApi, listApi){
    return{
        restrict: 'E',
        transclude: false,
        scope: {},
        link: function(scope, element, attrs){
            attrs.$observe('boatId', function(val){
                boatsApi.details(val).success(function(boat){
                    scope.boat = boat;
                    listApi.acTypes().success(function(acTypes){
                        scope.acTypes = acTypes;
                    });
                })
            });

            scope.update = function(){
                boatsApi.update(scope.boat).success(function(boat){

                })
            }
        },
        templateUrl: "/static/html/boat/edit.html"
    };
}]);