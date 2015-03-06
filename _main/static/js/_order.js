app.controller('baseFrmCtrl', function($scope, $cookieStore, orderApi, boatsApi){
  	$scope.hasError = function(field, validation){
	    if(validation){
      		return ($scope.form[field].$dirty && $scope.form[field].$error[validation]) || ($scope.submitted && $scope.form[field].$error[validation]);
	    }
	    return ($scope.form[field].$dirty && $scope.form[field].$invalid) || ($scope.submitted && $scope.form[field].$invalid);
  	};
});

app.controller('bookCtrl', function($scope, $controller, $location, $cookieStore, orderApi){
	$controller('baseFrmCtrl', {$scope: $scope}); 

	$scope.submit = function(){
		$scope.order.boat_id = $scope.boat.id;
		$scope.order.price_id = $scope.boat.price.id;
		$scope.order.total = $scope.boat.price.total;
		$scope.submitted = true;
		orderApi.create($scope.order).success(function(result){
			if(result.status === true){
				$scope.order.success = result.msg;
			} else {
				$scope.order.error = result.msg;
			}
		}).error(function(){
			alert("Unable to connect to server");
		});
	};

	if($cookieStore.get('order') && $cookieStore.get('boat')){
    	$scope.order = $cookieStore.get('order');
    	$scope.boat = $cookieStore.get('boat');
    	$scope.order.date = new Date($scope.order.date);
    } else {
    	$location.path('/');
    }
	$scope.order.name='arun';
 	$scope.order.email='arunghosh@gmail.com';
 	$scope.order.phone=9544440104;
 	$scope.order.city='kochi';
 	$scope.order.state='kerala';
 	$scope.order.address='palarivattom';
});


app.controller('cancelCtrl', function($scope, $controller, orderApi){
	$controller('baseFrmCtrl', {$scope: $scope}); 
	function init(){
		$scope.btnTxt ='Cancel Order';
		$scope.cancel = { order_id:14, user_email:"arunghosh@gmail.com"};
		$scope.response = {};
		$scope.date = new Date();
	}

	$scope.cancelOrder = function(){
		$scope.submitted = true;
		orderApi.cancel($scope.cancel).success(function(result){
			if(result.status === true){
				$scope.response = result;
				$scope.msg = "";
				$scope.btnTxt ='Confirm Cancellation';
			} else{
				$scope.msg = result.msg;
			}
			$scope.cancel.step = result.step;
		});
	};

	init();
});
