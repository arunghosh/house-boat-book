app.controller('addReviewCtrl', function($scope, $controller, $location, orderApi){
	$controller('baseCtrl', {$scope: $scope}); 
	
	$scope.review = {
		food: 3,
		cleanliness: 3,
		ambience: 3,
		order_id: $location.hash()
	};

	$scope.update = function(){
		orderApi.addReview($scope.review).success(function(){

		});
	};
});
