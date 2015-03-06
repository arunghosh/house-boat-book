app.config(function($routeProvider){
    $routeProvider
    .when('/orders',
    {
        templateUrl:common.getHtmlUrl('order/list'),
    })
    .when('/',
    {
        templateUrl:common.getHtmlUrl('bok/companies'),
    })
    .when('/cancel',
    {
        templateUrl:common.getHtmlUrl('bok/cpolicy'),
        controller:'cpolicyCtrl'
    });
});

app.controller('bokCtrl', function($scope, $location, $controller, manageApi, companyApi){
    $controller('baseDbCtrl', {$scope: $scope}); 

    $scope.showCompany = function(company){
        window.location.href = "/company/#/?id=" + company.id;
    }

    function init(){
        $scope.routes = [
            { name:"Companies", url:"", icon:"th", selected: true, },
            { name:"Booking", url:"orders", icon:"usd" },
            { name:"Cancel Policy", url:"cancel", icon:"ban-circle" },        
        ];

        companyApi.list().success(function(companies){
            $scope.companies = companies;
        });

	    manageApi.orders().success(function(orders){
	        $scope.orders = orders;
	    });

        $scope.refreshSelection();
    }

    init();
});


// app.controller('cpolicyCtrl', function($scope, $controller, $location, boatsApi){
//     $controller('baseDbCtrl', {$scope: $scope}); 

//     var cpc = {};

//     boatsApi.cPolicyCommon().success(function(policies){
//         cpc.policies = policies;
//         sort(policies);
//     })

//     cpc.edit = function(policy){
//         if(policy === undefined){
//             policy = {
//                 days: 0,
//                 percent: 100
//             };
//         }
//         cpc.policy = policy;
//         cpc.error = null;
//     };

//     function sort(policies){
//         policies.sort(function(a,b){
//             return (a.days > b.days) ? 1 : (b.days > a.days ? -1 : 0)
//         })      
//     }

//     function validate(){
//         var temp = cpc.policies.slice().reverse();
//         cpc.validation = null;
//         if(temp.length > 1){
//             if(temp[0].days - temp[1].days !== 1)
//             {
//                 cpc.validation = "The cancellation policy is invalid since policy for day " + (temp[0].days + 1) + " or " + (temp[0].days - 1) + " is missing. Common Policies will be used.";
//             }
//         }
//     }

//     cpc.update = function(){
//         boatsApi.updateCPolicyCommon(cpc.policy).success(function(result){
//             if(result.status == true) {
//                 cpc.policies.remove(cpc.policy);
//                 cpc.policies.push(result.data);
//                 cpc.policy = null;
//                 sort(cpc.policies);
//                 validate();
//             } else {
//                 cpc.error = result.msg; 
//             }
//         })
//     };
//     $scope.cpc = cpc;
// });
