angular.module('sadb')
    .controller('taxonomyController', taxonomyController);

function taxonomyController($scope,$http,$routeParams,sadbService) {
var base_url = sadbService.getAPIBaseUrl();
    $scope.taxons= [{ Taxonomy_Id: 7918, Common_name: 'Spotted gar' },
                   {Taxonomy_Id: 2, Common_name: 'second' },
                   {Taxonomy_Id: 3, Common_name: 'third' },
                   {Taxonomy_Id: 4, Common_name: 'fourth' },
                   {Taxonomy_Id: 5, Common_name: 'fifth' }];
    function select_taxon(taxon) {
        return taxon.Taxonomy_Id == $routeParams.taxonomy;
    }
    $scope.taxonomy= $scope.taxons.filter(item => item.Taxonomy_Id == $routeParams.taxonomy)[0]
    console.log($scope.taxonomy)

    $scope.get_taxon = function () {
        $http({
            url: base_url+'/api/taxonomy_list',
            params: {taxon_id:$routeParams.taxonomy},
            method: 'GET'
        }).then(
            function (response) {
                $scope.gene_list_count = response.data.gene_list_count;
                $scope.gene_list = response.data.gene_list;
            }
        )
    };
    $scope.get_taxon();

    $scope.update_taxon = function (test,page,size) {
        console.log("work")
        $http({
            url: base_url+'/api/taxonomy_list',
            params: {taxon_id:$routeParams.taxonomy,page:page},
            method: 'GET'
        }).then(
            function (response) {
                $scope.gene_list_count = response.data.gene_list_count;
                $scope.gene_list = response.data.gene_list;
            }
        )
    };

}
