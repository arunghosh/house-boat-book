var common = new function() {

    this.monthNames = [ "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December" ];
    this.weekDays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

    this.TEMPLATE_URL = "/static/html/";

    this.getHtmlUrl = function(template){
        return this.TEMPLATE_URL + template + ".html";
    };


    this.withCommas = function(x){
        return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    };

    this.readCookie = function(name){
        var nameEQ = name + "=";
        var ca = document.cookie.split(';');
        for(var i=0;i < ca.length;i++) {
            var c = ca[i];
            while (c.charAt(0)==' ') c = c.substring(1,c.length);
            if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
        };
        return null;
    }

    this.range = function(min, max) {
        var result = [];
        min = parseInt(min); //Make string input int
        max = parseInt(max);
        for (var i = min; i < max; i++) result.push(i);
        return result;
    };

    this.swap = function(a,b){
        temp = a;
        a = b;
        b = temp;
    };
};

Array.prototype.contains = function(item){
    for(var i = 0; i < this.length; i++){
        if(this[i] == item){
            return true;
        }
    }
    return false;   
};

Array.prototype.getById = function(id){
    for(var i = 0; i < this.length; i++){
        if(this[i].id == id){
            return this[i];
        }
    }
    return null;   
};

Array.prototype.remove = function(item){
    var index = this.indexOf(item);
    if(index > -1) this.splice(index,1);
};

// Array.prototype.removeById = function(id){
//     var index = this.indexOf(item);
//     if(index > -1) this.splice(index,1);
// };

Array.prototype.distinct = function(){
    return this.reduce(function(o,i){
        if(!o.contains(i)) o.push(i);
        return o;
    },[]).sort();
};

Date.prototype.getStr = function(){
    return this.getFullYear() + "-" + (this.getMonth() + 1) + "-" + this.getDate()
}


var app = angular.module('app', ['ngQuickDate', 'ngCookies', 'ngRoute', 'ngAnimate']);

app.config(function($interpolateProvider, $httpProvider) {
    $httpProvider.defaults.headers.post['X-CSRFToken'] = common.readCookie('csrftoken');
});

app.config(function(ngQuickDateDefaultsProvider) {
  return ngQuickDateDefaultsProvider.set({
    buttonIconHtml: '<span class="glyphicon glyphicon-calendar"></span>',
  });
});

app.filter("date_mdy", function() {
    return function(input) {
        var arr = input.split("T");
        return arr[0].replace(new Date().getFullYear(), "");
    };
});

app.filter("inr", function() {
    return function(input) {
        return "₹ " + input;
    };
});

app.filter("tickicon", function() {
    return function(status) {
        if(status == null) return "";
        return status === true ? "green glyphicon glyphicon-ok" : "red glyphicon glyphicon-remove";
    };
});

app.filter("inr_int", function() {
    return function(input) {
        if(input){
            return "₹ " + input.split(".")[0];
        }
        return "--";
    };
});

app.filter('range', function() {
    return function(input, min, max) {
        min = parseInt(min); //Make string input int
        max = parseInt(max);
        for (var i = min; i <= max; i++) input.push(i);
        return input;
    };
});

app.directive('modalDialog', function() {
  return {
    restrict: 'E',
    scope: {
      show: '='
    },
    replace: true, // Replace with the template below
    transclude: true, // we want to insert custom content inside the directive
    link: function(scope, element, attrs) {
        scope.dialogStyle = {};
        scope.title = attrs.title;
        if (attrs.width) scope.dialogStyle.width = attrs.width;
        if (attrs.height) scope.dialogStyle.height = attrs.height;
        scope.hideModal = function() {
            scope.show = false;
        };
    },
    templateUrl: "/static/html/common/modal.html"
  };
});

app.directive('orderDetails',['orderApi', function(orderApi){
    return{
        restrict: 'E',
        transclude: false,
        scope: {},
        link: function(scope, element, attrs){
            attrs.$observe('orderId', function(val){
                if(val){
                    orderApi.details(val).success(function(order){
                        scope.order = order;
                    });
                }
            })
        },
        templateUrl: "/static/html/order/details.html"
    };
}]);


app.directive('orderCreate',['orderApi', 'priceApi', 'boatsApi' , function(orderApi, priceApi, boatsApi){
    return{
        restrict: 'E',
        transclude: false,
        scope: {},
        link: function(scope, element, attrs){
            scope.order = {
                boat_id: attrs.boatId,
                // date: attrs.date ? attrs.date : new Date(),
                no_child: 0,
            };

            scope.order.name='arun';
            scope.order.email='arunghosh@gmail.com';
            scope.order.phone=9544440104;
            scope.order.city='kochi';
            scope.order.state='kerala';
            scope.order.address='palarivattom';

            attrs.$observe('date', function(val){
                scope.order.date = val ? new Date(val) : new Date();
                refrehPrice();
            });

            scope.submit = function(){
                orderApi.create(scope.order).success(function(result){
                    scope.error = null;
                    if(result.status === true){
                        scope.success = result.msg;
                    } else {
                        scope.error = result.msg;
                    }
                }).error(function(){
                    alert("Unable to connect to server");
                });
            };

            boatsApi.details(scope.order.boat_id).success(function(boat){
                scope.boat = boat;
                scope.order.no_adult = boat.no_adult;
                scope.$watch("order.no_child", refreshTotal);
                scope.$watch("order.no_adult", refreshTotal);
            });

            function refreshTotal(){
                if(scope.price && scope.boat){
                    var order = scope.order;
                    var b = scope.boat;
                    var price = scope.price;
                    var total = Number(price.base) + order.no_child * price.child;
                    total += (order.no_adult > b.no_adult) ? (order.no_adult - b.no_adult) * price.adult : 0;
                    scope.order.total = total;
                }
            };
            
            scope.$watch("order.date", refrehPrice());

            function refrehPrice(){
                if(scope.order.date){
                    priceApi.forBoatbyDate(scope.order.date, scope.order.boat_id).success(function(price){
                        scope.order.price_id = price.id;
                        scope.price = price;
                        scope.order.total = price.base;
                        refreshTotal();
                    });
                }
            }
        },
        templateUrl: "/static/html/order/create.html"
    };
}]);

app.directive('orderList',['orderApi', function(){
    return{
        restrict: 'E',
        transclude: false,
        scope: {},
        link: function(scope, element, attrs){
            
            scope.$parent.$watch(attrs.list, function(newVal, oldVal){
                if(newVal) scope.orders = newVal;
            });

            scope.showOrder = function(order){
                scope.order = order;
            }

        },
        templateUrl: "/static/html/order/list.html"
    };
}]);

app.directive('ngRating', function() {
    return {
        restrict: 'E',
        transclude: false, 
        scope: {},
        link: function(scope, element, attrs){
            scope.range = scope.$parent.getArray(5);
            scope.value = scope.$parent.review[attrs.model];
            scope.set = function(val){
                scope.value = val + 1;
                scope.$parent.review[attrs.model] = scope.value;
            }
        },
        templateUrl: "/static/html/common/rating.html"
    };
});

app.directive('showRating', function() {
    return {
        restrict: 'E',
        transclude: false, 
        scope: {},
        link: function(scope, element, attrs) {
            scope.range = [1,1,1,1,1];
            scope.value = attrs.value;
        },
        template: "<ul class='span'><li ng-repeat='n in range track by $index' class='glyphicon glyphicon-star rating' ng-class='{checked:$index < value}'></li></ul>"
    };
});

app.directive('busy', function() {
  return {
    restrict: 'E',
    scope: {
      show: '='
    },
    replace: true, // Replace with the template below
    transclude: true, // we want to insert custom content inside the directive
    link: function(scope, element, attrs) {
        scope.dialogStyle = {};
        scope.hideModal = function() {
            scope.show = false;
        };
    },
    templateUrl: "/static/html/common/busy.html"
  };
});


app.factory('searchApi', function($http){
    var base = '/search/api/';
    return {
        boats : function(data){
            return $http.post('/search/', data);
        },
        boatIds : function(data){
            return $http.post('/search/ids/', data);
        },
    };
});


app.factory('orderApi', function($http){
    var base = '/order/';
    return {
        create : function(data){
            var date = data.date;
            data.date_str = date.getStr();
            return $http.post(base + 'create/', data);
        },
        cancel : function(data){
            return $http.post(base + 'cancel/', data);
        },
        addReview : function(data){
            return $http.post(base + 'review/', data);
        },
        details : function(id){
            return $http.get(base + id);
        },
    };
});


app.factory('listApi', function($http){
    var base = '/list/';
    return {
        amenities : function(){
            return $http.get(base + "amenities/");
        },
        acTypes : function(){
            return $http.get(base + "ac_types/");
        },
    };
});

app.factory('priceApi', function($http){
    var apiBase = '/api/prices/';
    var base = '/price/';
    return {
        byDate: function(date){
            return $http.get(base + "date/" + date.getStr() + "/");
        },
        forBoatbyDate: function(date, boatId){
            return $http.get(base + "boat/" + boatId + "/" + date.getStr() + "/");
        },
        forBoat: function(boatId){
            return $http.get(base + "boat/" + boatId + "/");
        },
        month: function(boatId, year, month){
            return $http.get(base + "month/" + boatId + "/" + year + "/" + month + "/");
        },
        updateSeason : function(price){
            var price = angular.copy(price);
            price.date_from = price.date_from.toString().length > 12 ?  price.date_from.getStr() : price.date_from;
            price.date_to = price.date_to.toString().length > 12 ?  price.date_to.getStr() : price.date_to;
            return $http.post(base + "season/", price);   
        },
        updateBase : function(price){
            return $http.post(base + "base/", price);   
        },
    };
});

app.factory('boatsApi', function($http){
    var base = '/boats/';
    return {
        booked: function(date){
            return $http.get(base + "booked/" + date.getStr() + "/");
        },
        active: function(){
            return $http.get(base + "active/");
        },
        details: function(id){
            return $http.get("/api/boats/" + id + "/");
        },
        updateAmenities: function(data){
            return $http.post(base + "amenities/update/", data);
        },
        datePolicy: function(boat, date){
            return $http.get(base + boat.id +  "/policies/" + date.getStr() + "/");
        },
        cPolicy: function(boatId){
            return $http.get(base + boatId +  "/c_policy/");
        },
        updateCPolicy: function(data, boatId){
            if(boatId === undefined){
                return $http.post(base + "c_policy/", data);
            } else {
                return $http.post(base + boatId +  "/c_policy/", data);
            }
        },
        cPolicyCommon: function(){
            return $http.get(base + "c_policy/");
        },
        reviews: function(boatId, date){
            return $http.get(base + boatId +  "/reviews/");
        },
        mtncs: function(boatId){
            return $http.get(base + boatId +  "/maintenance/");
        },
        orders: function(boatId){
            return $http.get(base + boatId +  "/orders/");
        },
        update: function(data){
            return $http.post(base + "update/", data);
        },
        updateMtnc: function(data, boatId){
            var data = angular.copy(data);
            data.date_from = data.date_from.toString().length > 12 ?  data.date_from.getStr() : data.date_from;
            data.date_to = data.date_to.toString().length > 12 ?  data.date_to.getStr() : data.date_to;
            return $http.post(base + boatId +  "/maintenance/", data);
        },

    };
});

app.factory('companyApi', function($http){
    var base = '/company/';
    return {
        self : function(id){
            return $http.get(base + "/self/");
        },
        details : function(id){
            return $http.get("/api/companies/" + id + "/");
        },
        list : function(){
            return $http.get("/api/companies/");
        },
        boats : function(id){
            return $http.get(base + id + "/boats/");
        },
        orders : function(id){
            return $http.get(base + id + "/orders/");
        },
        upcomingOrders : function(id){
            return $http.get(base + id + "/orders/upcoming/");
        },
        owners : function(id){
            return $http.get(base + id + "/owners/");
        },
    };
});

app.factory('manageApi', function($http){
    var base = '/manage/';
    return {
        boats : function(){
            return $http.get(base + "boats/");
        },
        orders : function(){
            return $http.get(base + "orders/");
        },
        menus : function(){
            return $http.get(base + "menus/");
        },
    };
});


app.controller('baseCtrl', function($scope){
    $scope.getArray = function(num) {
        return new Array(num);   
    };
});


app.controller('baseDbCtrl', function($scope, $location, $templateCache, orderApi){

    $scope.routes = [];

    $scope.urlId = $location.search().id;

    $scope.getUrlId = function(){
        return $location.search().id;
    }

    $scope.show = function(r){
        $location.path(r.url);
        $scope.refreshSelection();
    }

    $scope.refreshSelection = function(){
        $scope.routes.map(function(r){
            r.selected = r.url === $location.path().replace("/", "");
        });
    }
});


app.controller('cpolicyCtrl', function($scope, $controller, $location, boatsApi){
    $controller('baseDbCtrl', {$scope: $scope}); 
    var boatId = $scope.urlId;

    var cpc = {};

    if(boatId){
        boatsApi.cPolicy(boatId).success(function(policies){
            cpc.policies = policies;
            sort(policies);
            validate();
        });

        boatsApi.cPolicyCommon().success(function(policies){
            cpc.common = policies;
            sort(policies);
        });
    } else {
        boatsApi.cPolicyCommon().success(function(policies){
            cpc.policies = policies;
            sort(policies);
            validate();
        });
    }


    cpc.edit = function(policy){
        if(policy === undefined){
            policy = {
                days: 0,
                percent: 100
            };
        }
        cpc.policy = policy;
        cpc.error = null;
    };

    function sort(policies){
        policies.sort(function(a,b){
            return (a.days > b.days) ? 1 : (b.days > a.days ? -1 : 0)
        })      
    }

    function validate(){
        var temp = cpc.policies.slice().reverse();
        cpc.validation = null;
        if(temp.length > 1){
            if(temp[0].days - temp[1].days !== 1)
            {
                cpc.validation = "The cancellation policy is invalid since policy for day " + (temp[0].days + 1) + " or " + (temp[0].days - 1) + " is missing. Common Policies will be used.";
            }
        }
    }

    cpc.update = function(){
        boatsApi.updateCPolicy(cpc.policy, boatId).success(function(result){
            if(result.status == true) {
                cpc.policies.remove(cpc.policy);
                cpc.policies.push(result.data);
                cpc.policy = null;
                sort(cpc.policies);
                validate();
            } else {
                cpc.error = result.msg; 
            }
        })
    };
    $scope.cpc = cpc;
});
