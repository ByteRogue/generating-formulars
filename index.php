<?php


require_once __DIR__ . '/vendor/autoload.php';

$page = 1;

$ROOT = 'cirih';

require_once $ROOT."\\out$page.php";

$mpdf = new mPDF();
 $mpdf->ignore_invalid_utf8 = true;
$mpdf->SetDisplayMode('fullpage');

$f = $page;
if ($page < 10)
	$f = '0'.$page;

$dashboard_pdf_file = "$ROOT\\Formular $page\\Formular$f.pdf";

function get_data($num) {
	return "$num";
}

$mpdf->SetImportUse();

$pagecount = $mpdf->SetSourceFile($dashboard_pdf_file);
$mpdf->WriteHTML('
.field {
	
	position:absolute;
}
.left {
	writing-mode:tb-rl;
    -webkit-transform:rotate(90deg);
    -moz-transform:rotate(90deg);
    -o-transform: rotate(90deg);
    -ms-transform:rotate(90deg);
    transform: rotate(90deg);
	text-align:left;
	//background-color:rgba(120,120,220,0.5);
}
.right {

	text-align:right;
	//background-color:rgba(220,120,120,0.5);
	
}

.data-right {
	padding-right: 0.1 in;
}

.data-left {
	padding-left: 0.1 in;
}

.date {
	text-align:right;
	// font-size:2.0in;
	// font-family: Courier;
	// //background-color:rgba(255,255,120,0.5);
	// letter-spacing:0.35in;
}


.center {
	text-align:center;
	//background-color:rgba(120,220,120,0.5);
}
',1);
for ($i = 1; $i <= $pagecount; $i++) {
	if ($page== 2 && $ROOT == 'formulari' && $i == 2) {
		$mpdf->AddPage('L');
	} else {
		$mpdf->AddPage();
	}
   

   	if ($html[$i-1])
   		$mpdf->WriteHTML($html[$i-1],2);


   $import_page = $mpdf->ImportPage($i);

   $mpdf->UseTemplate($import_page);

}

$nazivPDF = "izlaz$page.pdf";
$mpdf->Output("$ROOT/PDFs/$nazivPDF", 'F');
