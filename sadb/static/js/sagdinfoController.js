angular.module('sadb')
    .controller('sagdinfoController', sagdinfoController);

function sagdinfoController($scope,$http,$routeParams,sadbService) {
    var base_url = sadbService.getAPIBaseUrl();
    $(function () { $("[data-toggle='tooltip']").tooltip(); });
    $scope.get_sagd=function () {
        $scope.sagd_id=$routeParams.sagd_id
        $http({
            url: base_url+'/api/get_sagd_id',
            params: {sagd_id:$routeParams.sagd_id},
            method: 'GET'
        }).then(
            function (response) {
                console.log(response);
                $scope.items = response.data;
            }
        )
        $http({
            url: base_url+'/api/get_sagd_id_info',
            params: {sagd_id:$routeParams.sagd_id},
            method: 'GET'
        }).then(
            function (response) {
                console.log(response);
                $scope.sagd_info = response.data;
            }
        )
    }
    $scope.get_sagd()

}