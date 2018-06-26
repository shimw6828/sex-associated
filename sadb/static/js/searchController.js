angular.module('sadb')
    .controller('searchController', searchController);

function searchController($scope,$http,$routeParams,sadbService) {
    var base_url = sadbService.getAPIBaseUrl();
    $scope.loadcomp=false
    $(function () { $("[data-toggle='tooltip']").tooltip(); });
    $scope.fetch_gene = function(){
        var update ="not update"
         $http({
            url: base_url+'/api/search',
            params: {query:$routeParams.query},
            method: 'GET'
        }).then(
            function (response) {
                console.log(response);
                $scope.gene_list_count = response.data.gene_list_count;
                $scope.gene_list = response.data.gene_list;
                console.log($scope.gene_list)
                $scope.loadcomp=true
                if($scope.gene_list_count==0){
                    window.open(base_url+"#!/noResult","_self")
                }
            }
        )
    };
    $scope.padjs=[0.05,0.01,0.001,0.0001]
    $scope.fetch_gene();

    $scope.padjchange =function (padjvalue) {
        padj=padjvalue
        $scope.update_all_gene()
    }
    padj=""
    $scope.update_gene = function(test,page,size){
        $scope.loadcomp=false
        console.log(padj)
        var update="update"
         $http({
            url: base_url+'/api/search',
            params: {query:$routeParams.query,page:page,update:update,padj:padj},
            method: 'GET'
        }).then(
            function (response) {
                $scope.gene_list = response.data.gene_list;
                $scope.loadcomp=true
                padjchane=false
            }
        )}
    $scope.update_all_gene = function(test,page,size){
        $scope.loadcomp=false

        var update ="not update"
        console.log($routeParams.query)
        $http({
            url: base_url+'/api/search',
            params: {query:$routeParams.query,page:page,update:"not update",padj:padj},
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






