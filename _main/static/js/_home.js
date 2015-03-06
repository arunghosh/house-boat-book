app.config(function($routeProvider){
    $routeProvider
        .when('/',
        {
            templateUrl:common.getHtmlUrl('public/home'),
            controller:'homeCtrl'
        })
        .when('/book',
        {
            templateUrl:common.getHtmlUrl('public/book'),
            controller:'bookCtrl'
        })
        .when('/search/',
        {
            templateUrl:common.getHtmlUrl('public/search'),
            controller:'searchCtrl'
        });
});


app.controller('homeCtrl', function($scope, $location, $cookieStore){

    $scope.text = document.querySelector('body').className.indexOf('abcd');
    debugger;
    $scope.showSearch = function(){
        $cookieStore.put('order', {date:$scope.date});
        $location.path('search')
    };
});
