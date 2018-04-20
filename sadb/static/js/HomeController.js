
angular.module('sadb')
    .controller('HomeController', HomeController);
function HomeController($scope,$http,$window,$routeParams,sadbService) {
    console.log("HomeController loaded");


    var gene_name;
    var name_list=[];
    var flag=0
    var base_url = sadbService.getAPIBaseUrl();
    var subjects=["rs1001021","rs2642","rs7069","NONHSAT000024.2","ENST00000515242"];
    $('#search').typeahead({source: subjects});
    $(document).keyup(function(event){
        if(event.keyCode ==13){
            $("#search_button").trigger("click");
        }
    });
    $scope.search_query = function () {
        var query_item = $('#search').val();
        if(/[@#\$%\^&\*]+/g.test(query_item)){
            alert("Invalid input");
            flag=1;
            history.back();
        }
        if(flag==0){
            if(query_item.indexOf("SR")==0){
                $scope.filter_sra(query_item)
            }
            else {
                $scope.filter_gene(query_item)
            }
        }


        }


    $scope.filter_sra = function (query_sra) {
        window.open(base_url+"#!/sra_info?sra="+query_sra,"_self")
    }
    $scope.filter_gene = function (query_gene) {
        window.open(base_url+"#!/gene_info?gene_id="+query_gene,"_self")
    }
    }