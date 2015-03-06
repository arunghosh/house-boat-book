
app.config(function($routeProvider){
    $routeProvider
    .when('/',
    {
        templateUrl:common.getHtmlUrl('order/list'),
    })
    .when('/users',
    {
        templateUrl:common.getHtmlUrl('company/users'),
    })
    .when('/boats',
    {
        templateUrl:common.getHtmlUrl('company/boats'),
    });
});


app.controller('companyCtrl', function($scope, $location, $controller, companyApi){
    $controller('baseDbCtrl', {$scope: $scope}); 
    
    $scope.showBoat = function(boat){
        window.location.href = "/boats/#/?id=" + boat.id;
    }

    function init(){
        var id = $scope.urlId;
        if(id) {
            companyApi.details(id).success(function(company){
                $scope.company = company;
                fillData();
            });        
        } else {
            companyApi.self().success(function(company){
               $scope.company = company; 
               fillData();
            });
        }

        function fillData(){
            var id = $scope.company.id;
            companyApi.boats(id).success(function(boats){
                $scope.boats = boats;
            });
            companyApi.upcomingOrders(id).success(function(orders){
                $scope.orders = orders;
            });
            companyApi.owners(id).success(function(owners){
                $scope.users = owners;
            });
        }

        $scope.refreshSelection();
    }

    // $scope.show = function(route){
    //     $scope.routes.map(function(r){
    //         r.selected = false;
    //     });
    //     route.selected = true
    // }

    $scope.routes = [
        {
            name:"Booking",
            url:"",
            icon:"usd",
            selected: true,
        },
        {
            name:"Boats",
            url:"boats",
            icon:"list",
        },        {
            name:"Users",
            url:"users",
            icon:"user"
        },
    ];

    init();
});
