angular.module('sadb')
    .controller('browseController', browseController);
// (function (ng) {
//     'use strict';
// var app = ng.module('ngLoadScript', []);
// app.directive('script', function() {
//     return {
//         restrict: 'E',
//         scope: false,
//         link: function(scope, elem, attr)
//         {
//             if (attr.type==='text/javascript-lazy')
//             {
//                 var s = document.createElement("script");
//                 s.type = "text/javascript";
//                 var src = elem.attr('src');
//                 if(src!==undefined)
//                 {
//                     s.src = src;
//                 }
//                 else
//                 {
//                     var code = elem.text();
//                     s.text = code;
//                 }
//                 document.head.appendChild(s);
//                 elem.remove();
//             }
//         }
//     };
// });
// }(angular));

function browseController($scope,$http,$routeParams,sadbService) {
    var base_url = sadbService.getAPIBaseUrl();
    $scope.browsetest = function () {
        console.log("ok");
        var taxonomy = "7918";
        window.open(base_url+"#!/taxonomy?taxonomy="+taxonomy,"_self")


    }


    


}

