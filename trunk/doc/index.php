<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"> 
<html xmlns="http://www.w3.org/1999/xhtml"> 
 
<html> 
<head> 
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" /> 
<title>Documentation - GeoRemindMe Web App</title> 
 
<link rel="stylesheet" href="http://www.georemindme.com/static/webapp/style/screen.css" type="text/css" media="screen, projection" /> 
<link rel="stylesheet" href="http://www.georemindme.com/static/webapp/style/style.css" type="text/css" media="screen, projection" /> 
<link rel="stylesheet" href="http://www.georemindme.com/static/webapp/style/print.css" type="text/css" media="print" /> 
 
 
 
<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.5.1/jquery.min.js"></script> 
<script type="text/javascript" src="http://www.georemindme.com/static/webapp/js/jquery.preload-1.0.8-min.js"></script> 
 
 
<script type="text/javascript" src="http://www.georemindme.com/webapp/static/webapp/js/static.js"></script> 
 
<!-- Loading lightbox plugin--> 
<script type="text/javascript" src="http://www.georemindme.com/webapp/static/webapp/js/jquery.lightbox-0.5.js"></script> 
<link rel="stylesheet" type="text/css" href="http://www.georemindme.com/webapp/static/webapp/style/jquery.lightbox-0.5.css" media="screen" /> 
 <script type="text/javascript"> 
    $(function() {
        $('.screenshots a').lightBox();
        
           $('input[type=submit]').click(function(e){
               e.preventDefault();
               
               if (!echeck($('#user-email').val()))
               {
                    $("#wait-mask").hide();
                    $('#sentMsg').removeClass("msgOK").addClass("msgNoOK");$('#sentMsg span').text("Email incorrecto");
                    return;
                }
               
               $("#wait-mask").show();
               $.ajax({
                   url: AJAX_URL+"keep-up-to-date/",
                   type: "post",
                   data: $("#form-keep-up-to-date").serialize(),
                   async:true,
                   success: function(){ $("#wait-mask").hide(); $('#sentMsg').removeClass("msgNoOK").addClass("msgOK");$('#sentMsg span').text("¡El mensaje se ha enviado correctamente!");$('#msg,#userEmail').val('');},
                   error: function(){ $("#wait-mask").hide(); $('#sentMsg').removeClass("msgOK").addClass("msgNoOK");$('#sentMsg span').text("Se ha producido un error al enviar el mensaje");}           
                   });
            
        });
    });
 </script> 
 
 
<!--
<script type="text/javascript" src="js/jquery-1.4.2.min.js"></script> 
--> 
 
<script type="text/javascript" src="../src/webapp/static/webapp/js/base.js"></script> 
 
<!--[if IE]>
<link rel="stylesheet" href="../src/webapp/static/webapp/style/ie.css" type="text/css"
media="screen, projection" />
<![endif]--> 
 
<!--[if lt IE 9]>
<script src="https://html5shim.googlecode.com/svn/trunk/html5.js" type="text/javascript"></script>
<![endif]--> 
 
<style type="text/css">
   .content-box blockquote{
       color: #222222;
       font-style: normal;
       font-weight: normal;
       margin-bottom: 0;
       margin-top: 0;
   }
   .content-box div{
      font-weight: normal;
   }
   #main-container p {
      1.5em
   }
   .content-box ul li{
      display: list-item;
      list-style: disc outside none;
      margin-left: 30px;
   }
   td{
      border:0;
   }
   .tab1{
      padding-left:0px;
   }
   .tab2{
      padding-left:15px;
   }
   .tab3{
      padding-left:30px;
   }
   article h3{
      margin-top: 10px;
   }
</style>
 
</head> 
 
<body> 
 
   <div id="wait-mask"></div> 
   <div class="container" id="documentation">     
      <header> 
         <span id="logo"><a href="/" title="Ir volando a la página de inicio. Pio! Pio!"><img src="http://www.georemindme.com/static/webapp/img/logoHeader.png" alt="GeoRemindMe"></a></span> 
         <nav> 
            <h1>Webapp Developers center</h1>
            (<em>Last update on <?php echo date("d/m/Y H:i:s", filectime('index.php')); ?></em>)
         </nav> 
      </header> 
 
   <div id="main-container">   
      <div id="col-left"> 
         <!-- Content index with animated scroll--> 
         <ul id="content-index"> 
            <li><a href="#documentation" class="anchor separator" id="back-to-top">Back to top</a></li> 
            <li><a href="#introduction" class="anchor separator">Introduction</a></li> 
            <li><a href="#serverarchitecture" class="anchor separator">Server architecture</a></li> 
            <li><a href="#androidapp" class="anchor separator">Android application</a></li> 
         </ul> 
         <!-- En content index--> 
      </div> 
      <section id="col-right"> 
         <article class="content-box" id="introduction"> 
            <div> 
            <h2>Introduction</h2> 
            <p>This documentation aims to help new developers to understand how the project has been built in order to be able to help you to contribute with the project.</p> 
            
            <p>It has multiple versions, not just a web client and a mobile app as you can see in this graphic:</p>
            <p style="text-align:center"><a href="common/First dia.png"><img src="common/First dia.png" style="width:250px;float:none"/></a></p>
            <p>There are also a commertial site, a web client for mobile devices, and in the future will be much more.<br>All of those applications are sincronized, so the way we are using to communicate and sincronize them is something like this:</p>
            <p style="text-align:center"><a href="common/Client-Server interaction.png"><img src="common/Client-Server interaction.png" style="width:250px;float:none"/></a></p>
            <p><a href="#documentation" class="back-to-top">Back to top</a></p> 
            </div> 
         </article> 
         
         
         
         
         <article class="content-box" id="serverarchitecture"> 
            <div> 
            <h2>Web application</h2> 
            <p>Responsable: Ruben (ruben@georemindme.com)</p>
            <p>If you want to contribute with the web application first of all you should understand how it works.</p>
            <p>As you maybe have read, the are several web applications, all of them almost independent, but despite that, they share some things, here you can read some tutorials:</p>

            <ul>
               <li><a href="webapp/install_and_deploy.txt">Learn how to run the local application on you local machine here.</a></li>
               <li><a href="webapp/generate_update_languages.txt">Learn how create new language files and set translations.</a> </li>
               <li><a href="webapp/AJAX use.txt">Learn how create to use the AJAX to sincronize with the application. </a> (Spanish)</li>
            </ul>
            <h3>Server side</h3>
            
            <p style="text-align:center"><img src="webapp/Estructura de clases.png"  style="width:250px;float:none" /></p>
            <p style="text-align:center"><img src="webapp/Models.png"  style="width:250px;float:none" /></p>
            
            <p style="text-align:center"><img src="webapp/Modulos aplicacion.png"  style="width:250px;float:none" /></p>
            
            <h3>Dashboard application (Client side)</h3>
            <p>It is the one that handles all the reminders on a big screen, its built on Django and you can see it here</p>
            <p style="text-align:center"><img src="webapp/Aplicaciones.png"  style="width:250px;float:none" /></p>
            
            <h3>Mobile application</h3>
            <h3>Promotional site</h3>
            <p><a href="#documentation" class="back-to-top">Back to top</a></p> 
            </div> 
         </article> 
         
         
         <article class="content-box" id="androidapp"> 
            <div> 
            <h2>Android application</h2>
            <p>Responsable: Fran (fran@georemindme.com)</p>
            <p>If you want to contribute with the Android application the first thing you should read are those documents:</p>
            <ul>
               <li><a href="android/style_guide_android.pdf">The style guide for the Android developers</a> (Spanish)</li>
               <li><a href="android/system_architecture.pdf">Which is the architecture of the Android App</a> (Spanish)</li>
            </ul>
            <p>Another diagram that shows the logic of the application.</p>
            <p style="text-align:center"><img src="android/logica-android.png" style="width:250px;float:none"/></p>
            
            <p><a href="#documentation" class="back-to-top">Back to top</a></p> 
            </div> 
         </article> 
      </section> 
    </div> 
 
</body> 
 
</html> 
