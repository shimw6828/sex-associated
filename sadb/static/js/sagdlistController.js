angular.module('sadb')
    .controller('sagdlistController', sagdlistController);

function sagdlistController($scope,$http,$routeParams,sadbService) {
    var base_url = sadbService.getAPIBaseUrl();
    $scope.padjs=[0.05,0.01,0.001,0.0001]
    $(function () { $("[data-toggle='tooltip']").tooltip(); });
    $scope.loadcomp=false
    $scope.get_sagd=function () {
        $http({
            url: base_url+'/api/get_sagd_list',
            params: {sagd_id:$routeParams.sagd_id},
            method: 'GET'
        }).then(
            function (response) {
                console.log(response);
                $scope.gene_list_count = response.data.gene_list_count;
                $scope.gene_list = response.data.gene_list;
                console.log($scope.gene_list_count)
                $scope.loadcomp=true
            }
        )
    }
    padj=""
    $scope.get_sagd()
    $scope.padjchange =function (padjvalue) {
        padjchane=true
        padj=padjvalue
        $scope.update_all_gene()
    }
    $scope.update_gene = function(test,page,size){
        $scope.loadcomp=false
        console.log(min)
        if(min){var min=$('#min_val').val()}
        if(max){var max=$('#max_val').val()}
        var update="update"
         $http({
            url: base_url+'/api/get_sagd_list',
            params: {sagd_id:$routeParams.sagd_id,page:page,update:update,padj:padj},
            method: 'GET'
        }).then(
            function (response) {
                $scope.gene_list = response.data.gene_list;
                $scope.loadcomp=true
            }
        )}
    $scope.update_all_gene = function(test,page,size){
        $scope.loadcomp=false
        var update ="not update"
        $http({
            url: base_url+'/api/get_sagd_list',
            params: {sagd_id:$routeParams.sagd_id,page:page,update:"not update",padj:padj},
            method: 'GET'
        }).then(
            function (response) {
                $scope.gene_list = response.data.gene_list;
                $scope.gene_list_count = response.data.gene_list_count;
                $scope.loadcomp=true;
                console.log($scope.gene_list_count)
            }
        )
        }


}