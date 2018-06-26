"use strict";

angular.module('sadb',['ngRoute','bw.paging','tableSort','ui.select','ngSanitize','nsPopover'])
    .config(function($routeProvider){
        $routeProvider
            .when("/", {
                templateUrl: "/static/pages/home.html",
                controller: "HomeController"
            })
            .when("/sra_info",{
                templateUrl:"/static/pages/sra.html",
                controller: "SRAController"
            })
            .when("/taxonomy",{
                templateUrl:"/static/pages/taxonomy.html",
                controller: "taxonomyController"
            })
            .when("/search",{
                templateUrl:"/static/pages/search.html",
                controller: "searchController"
            })
            .when("/gene_info",{
                templateUrl:"/static/pages/gene_info.html",
                controller: "geneinfoController"
            })
            .when("/sagd_info",{
                templateUrl:"/static/pages/sagd_info.html",
                controller: "sagdinfoController"
            })
            .when("/sagd_list",{
                templateUrl:"/static/pages/sagd_list.html",
                controller: "sagdlistController"
            })
            .when("/browse_gene",{
                templateUrl:"/static/pages/browse_gene.html",
                controller: "browsegeneController"
            })
            .when("/noResult",{
                templateUrl:"/static/pages/noResult.html"
            })
            .when("/contact",{
                templateUrl:"/static/pages/contact.html"
            })
            .when("/drug",{
                templateUrl:"/static/pages/drug.html",
                controller: "drugController"
            }).when("/dataset",{
                templateUrl:"/static/pages/dataset.html",
                controller: "datasetController"
            })
            .when("/browse_species",{
                templateUrl:"/static/pages/browse_species.html",
                controller: "browseController"
            });
    })

    .service('sadbService',function () {
        this.getBrowserBaseUrl = function () {
            return "127.0.0.1";
            };
        this.getBrowserDataHubNaseUrl = function () {
            // return "192.168.0.101/sadb";
            return "0.0.0.0:3000";
        };
        this.getAPIBaseUrl = function () {
            //return "/sadb"
            return ""
        }
    })
    .controller('navigation', navigation);
    function navigation($scope,$http,$routeParams,sadbService) {

        $("input").keyup(function(event){
            if(event.keyCode ==13){
            $scope.search_query();
        }
    });

    var flag=0
    var base_url = sadbService.getAPIBaseUrl();
    $scope.search_query = function () {

        var query_item = $('#search').val();

        if(/[@#\$%\^&\*]+/g.test(query_item)){
            console.log(query_item);
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
            window.open(base_url+"#!/search?query="+query_gene,"_self")
        }

    }




