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
    $("input").keyup(function(event){
        if(event.keyCode ==13){
             $scope.update_taxon("test",1,15);
        }
    });


    $scope.update_taxon = function (test,page,size,sort) {
        console.log(sort)
        if ($scope.gene_list_count<15)
        {var filter_search = $('#filter_search_2').val();
         $('#filter_search').val("");
         $('#min').val("");
         var min=$('#min').val();
         $('#max').val("");
         var max=$('#max').val();}
        else
        {var filter_search = $('#filter_search').val();
        var min=$('#min').val();
        var max=$('#max').val()}

        console.log(filter_search)
        console.log(typeof(min))
        console.log(max)
        $http({
            url: base_url+'/api/taxonomy_list',
            params: {taxon_id:$routeParams.taxonomy,page:page,filter:filter_search,min:min,max:max},
            method: 'GET'
        }).then(
            function (response) {
                $scope.gene_list_count = response.data.gene_list_count;
                $scope.gene_list = response.data.gene_list;
            }
        )
    };

}
