<?php


require_once __DIR__ . '/vendor/autoload.php';


$page = 1;

$ROOT = 'st_galen';
$form = [];

function path($path) {
	return join(DIRECTORY_SEPARATOR, $path);
}

$mpdf = new mPDF();

$mpdf->WriteHTML('
body{
	font-family: "Myriad Pro";
	font-size: 8.1pt;
}
.field {
	font-weight: normal;
	position:absolute;
}
.left {
	font-weight: normal;
	text-align:left;
	//background-color:rgba(120,120,220,0.5);
}
.right {
	font-weight: bold;
	text-align:right;

	
}

.data-right {
	padding-right: 0.1 in;
}

.data-left {
	font-weight: normal;
	padding-left: 0.1 in;
	padding-right: 0.1 in;

}

.date {
	//background-color:red;
	font-weight: bold;
	text-align:right;

}


.center {
	text-align:center;

}
',1);
$all = glob($ROOT.DIRECTORY_SEPARATOR."Formular*.pdf");
//var_dump($all);
foreach (glob($ROOT.DIRECTORY_SEPARATOR."out[0-9][0-9].php") as $key => $f) {
	# code...
	echo $f.PHP_EOL;
	require_once($f);
	$form[$key] = $html;
	//echo $html;

	$dashboard_pdf_file = $all[$key];
	$mpdf->SetImportUse();

	$pagecount = $mpdf->SetSourceFile($dashboard_pdf_file);

	for ($i = 1; $i <= $pagecount; $i++) {
		if ($key == 1 && $i > 1)
			$mpdf->addPage('L');
		else 
			$mpdf->addPage();

	   	if ($form[$key][$i-1])
	   		$mpdf->WriteHTML($form[$key][$i-1],2);


	   $import_page = $mpdf->ImportPage($i);

	   $mpdf->UseTemplate($import_page);


	}

}
// $f = $page
// if ($page < 10)
// 	$f = '0'.$page;



function get_data($num) {
	return $num;
}

// $mpdf->SetImportUse();

// $pagecount = $mpdf->SetSourceFile($dashboard_pdf_file);



$mpdf->Output("$ROOT/generated.pdf", 'F');
