<?php
require '../../h2o/h2o.php';
require '../../templates/menu_sections.php';
h2o::load('i18n');

$var_template='licensing.html';
$var_title='Licensing information';
//None in this case
#$active_section= 'Community'; //Values= Names on ../templates/menu_sections.php

$template = new H2o('../../templates/'.$var_template, array(
    //'cache_dir' => dirname(__FILE__),
));

echo $template->render(array(
	'title'=> $var_title,
	'menu_items'=>$menu_sections,
	#'active_section'=>$active_section,
	)
);

