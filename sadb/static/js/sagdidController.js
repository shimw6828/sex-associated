angular.module('sadb')
    .controller('sagdidController', sagdidController);

function searchController($scope,$http,$routeParams,sadbService) {
    $scope.get_sagd=function () {
        $http({
            url: base_url+'/api/sagd',
            params: {gene_id:$routeParams.sagd_id},
            method: 'GET'
        }).then(
            function (response) {
                console.log(response);
                $scope.gene_list_count = response.data.gene_list_count;
                $scope.gene_list = response.data.gene_list;
            }
        )
    }

}