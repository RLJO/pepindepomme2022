
function callBackFrame(point){
Colissimo_lastRelaySelected= point

}

jQuery.extend(jQuery.fn, {
	frameColissimoOpen: function(params)
	{
		
		//Le conteneur
		var conteneur_widget_colissimo = this;
		
		//On recherche l'url du serveur
		
		var colissimo = jQuery;
		//var colissimo = $;
		
		
		
		
//		var url = colissimo('script[src*="jquery.plugin.colissimo"]').attr("src");
//		//console.log('url source = ' + url);
//		
//    	var indexpath = url.indexOf('widget-point-retrait',0);
//    	var urlColiposte = url.substring(0, indexpath-1);
    	
		var colissimo_widget_urlColiposte = params.URLColissimo;
    	
    	
    	
    	
		var colissimo_widget_lang = params.ceLang;
		var colissimo_widget_callBackFrame = params.callBackFrame;
		
		
		//Contrôle des parametres
		var colissimo_widget_codeRetour = 0;
		if(params.URLColissimo == null || params.URLColissimo == '')
		{
			colissimo_widget_codeRetour = 10;
		}
		if(params.ceCountryList == null || params.ceCountryList == '')
		{
			colissimo_widget_codeRetour = 10;
		}
		if(params.ceCountry == null || params.ceCountry == '')
		{
			colissimo_widget_codeRetour = 20;
		}
		if(params.ceLang == null || params.ceLang == '')
		{
			colissimo_widget_codeRetour = 30;
		}
		if(params.dyPreparationTime == null || params.dyPreparationTime == '')
		{
			colissimo_widget_codeRetour = 40;
		}
		
		var colissimo_widget_bootstrap_css_link = colissimo("<link>", { 
			rel: "stylesheet", 
			type: "text/css", 
			href: colissimo_widget_urlColiposte + "/widget-point-retrait/resources/css/bootstrap.colissimo.min.css" 
		});
		colissimo_widget_bootstrap_css_link.appendTo('head');
		colissimo("head").append('\n');
		
		var colissimo_widget_css_link = colissimo("<link>", { 
			rel: "stylesheet", 
			type: "text/css", 
			href: colissimo_widget_urlColiposte + "/widget-point-retrait/resources/css/mystyle.css" 
		});
		colissimo_widget_css_link.appendTo('head');  
		colissimo("head").append('\n');
		
		
		//console.log(jQuery.ui);
		
		
		var colissimo_widget_ui_css_link = colissimo("<link>", { 
			rel: "stylesheet", 
			type: "text/css", 
			href: colissimo_widget_urlColiposte + "/widget-point-retrait/resources/css/jquery-ui.colissimo.min.css" 
		});
		colissimo_widget_ui_css_link.appendTo('head');
		colissimo("head").append('\n');
		
		
		
//		var ui_css_link = colissimo("<link>", { 
//			rel: "stylesheet", 
//			type: "text/css", 
//			href: urlColiposte + "/widget-point-retrait/resources/css/jquery-ui.min-1.11.4.css" 
//		});
//		ui_css_link.appendTo('head');
//		colissimo("head").append('\n');
		
		if(typeof jQuery.ui == 'undefined')
		{
			
	//		var s = document.createElement("script");
	//		s.type = "text/javascript";
	//		s.src = urlColiposte + "/widget-point-retrait/resources/js/bootstrap.min.js";
	//		s.defer = true;
	//		colissimo("head").append(s);
	//		colissimo("head").append('\n');
			
			var colissimo_widget_sUI = document.createElement("script");
			colissimo_widget_sUI.type = "text/javascript";
			colissimo_widget_sUI.src = colissimo_widget_urlColiposte + "/widget-point-retrait/resources/js/jquery-ui.min-1.11.4.js";
			colissimo("head").append(colissimo_widget_sUI);
			colissimo("head").append('\n');

			//console.log(jQuery.ui);
		}
		
		//console.log('in integre les scripts pour la map');
		//console.log('map box');
		//console.log('t : ' + t);
		var colissimo_widget_mapbox = document.createElement("script");
		colissimo_widget_mapbox.type = "text/javascript";
		colissimo_widget_mapbox.src = "https://api.mapbox.com/mapbox.js/v2.2.4/mapbox.js";
		colissimo_widget_mapbox.defer = true;
		colissimo("head").append(colissimo_widget_mapbox);
		colissimo("head").append('\n');
		
		var colissimo_widget_mapbox_css_link = colissimo("<link>", { 
			rel: "stylesheet", 
			type: "text/css", 
			href:"https://api.mapbox.com/mapbox.js/v2.2.1/mapbox.css" 
		});
		colissimo_widget_mapbox_css_link.appendTo('head');
		colissimo("head").append('\n');
		
		
		//Les balises meta
		colissimo("head").append('<meta http-equiv="X-UA-Compatible" content="IE=edge">');
		colissimo("head").append('\n');
		colissimo("head").append('<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />');
		colissimo("head").append('\n');
		colissimo("head").append('<meta name="apple-mobile-web-app-capable" content="yes">');
		colissimo("head").append('\n');
		
		
		//console.log('FIN integre les scripts pour la map');
		
		var colissimo_widget_widget_url = colissimo_widget_urlColiposte + "/widget-point-retrait/index.htm";		
		var colissimo_widget_dataIndex = 'h1=' + colissimo_widget_lang + '&callBackFrame=' + colissimo_widget_callBackFrame + '&domain=' + colissimo_widget_urlColiposte + '&ceCountryList=' + params.ceCountryList + '&codeRetour=' + colissimo_widget_codeRetour + '&dyPreparationTime=' + params.dyPreparationTime + '&dyWeight=' + params.dyWeight + '&ceAddress=' + params.ceAddress + '&ceCountry=' + params.ceCountry+ '&ceZipCode=' + params.ceZipCode + '&token=' + params.token + '&idContainerWidget=' + conteneur_widget_colissimo.attr('id');
		
		colissimo.ajax({
			method :"POST",
		    url: colissimo_widget_widget_url,
		    data : colissimo_widget_dataIndex,
		    success: function (data) {
		    	
		    	conteneur_widget_colissimo.html(   data.replace('var colissimojQuery = jQuery.noConflict();', 'var colissimojQuery = jQuery;').replace('href="#"', '')  );
		    	
		    	//Le pays
//		    	if(params.ceCountry != null && params.ceCountry != '')
//		    	{
//		    		//console.log('pays par defaut : ' + params.ceCountry);
//		    		colissimo("#colissimo_widget_listePays").attr('value', params.ceCountry);
//		    	}
		    	
		    	
		    	
			    setTimeout( function() {
					
			    	
			    	
			    	
			    	
					 colissimojQuery.ajax({
						   type: "POST",
						   encoding:"UTF-8",
						   contentType: "application/x-www-form-urlencoded; charset=utf-8",
							   url: colissimo_widget_urlColiposte + '/widget-point-retrait/GetPays.htm',
							   data: "lang=" + colissimo_widget_lang + "&ceCountryList=" + params.ceCountryList + "&token=" + params.token,
						   success: function(msg){
					   	   
							   var data = msg.split(';');
							   
						    	//On modifie la liste
						    	populateCountry(data, params.ceCountry);

						   },
						    error : function(resultat, statut, erreur){
					    	
						    	//console.log(erreur); 
						    } 
					 });
			    	
			    	
			    	
			    	
			    	
			    	if(params.ceAddress != null && params.ceAddress != '')
			    	{
			    		colissimo("#colissimo_widget_Adresse1").val(params.ceAddress);
			    	}
			    	if(params.ceZipCode != null && params.ceZipCode != '')
			    	{
			    		colissimo("#colissimo_widget_CodePostal").val(params.ceZipCode);
			    	}
			    	if(params.ceTown != null && params.ceTown != '')
			    	{
			    		colissimo("#colissimo_widget_Ville").val(params.ceTown);
			    		
			    		
					    setTimeout( function() {
					    	colissimo_widget_loadingPointRetrait();
							}, 500 )
			    	}
			    	
					}, 500 )

		    },
		    error : function(resultat, statut, erreur){
		    	console.log(statut);
		    	console.log(erreur);
		    } 
		});
		var $ = jQuery;
		return this;
	},
	frameColissimoClose: function()
	{
		//Code du second plug-in ici
		//console.log('fermeture frame');
		return this;
	}
});

function colissimo_widget_loadingPointRetrait(){
	
	//console.log('co = ');
	//console.log(typeof(co));
	
	var p = jQuery("#colissimo_widget_listePays").val();
	
	console.log('Pays = ' + p);
	if(typeof(p) == 'undefined' || p == null){
		setTimeout(function(){colissimo_widget_loadingPointRetrait();}, 200); // Wainting the JS file is loaded
		//console.log('oym non charge, on attend....');
	}else{
		colissimo_widget_getPointsRetrait();
	}
}

function populateCountry(data, ceCountry)
{
	var colissimojQuery = jQuery;
	
	var paysValue = colissimojQuery("#colissimo_widget_listePays").attr('value');
	
	if(paysValue == null || paysValue == '' || paysValue == undefined)
	{
		paysValue = ceCountry;
	}
	
	   
	 for(i = 0; i < data.length-1 ; i++)
    {
		 if(data[i] == paysValue)
		 {
			colissimojQuery("#colissimo_widget_listePays").append("<option value='" + data[i] +"' selected='selected'>" + data[i+1] + "</option>"); 
		 } else {
		 	colissimojQuery("#colissimo_widget_listePays").append("<option value='" + data[i] +"'>" + data[i+1] + "</option>");
		 }
		 i++;
	 }
}
