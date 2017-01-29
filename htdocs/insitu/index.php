<?php
header("Last-Modified: " . gmdate("D, d M Y H:i:s") . " GMT");
header("Cache-Control: no-store, no-cache, must-revalidate");
header("Cache-Control: post-check=0, pre-check=0", false);
header("Pragma: no-cache");
header("Expires: Sat, 26 Jul 1997 05:00:00 GMT");

function human_filesize($bytes, $decimals = 2) {
    $size = array('','k','M','G','T','P','E','Z','Y');
    $factor = floor((strlen($bytes) - 1) / 3);
	if ( $factor <= 1 ) {
		$decimals = 0;
	}
    return sprintf("%.{$decimals}f", $bytes / pow(1024, $factor)) . @$size[$factor];
}
$curpath = "$_SERVER[REQUEST_URI]";
if (strpos($curpath, 'armv6') !== false) {
	$arm="armv6";
}else{
	$arm="armv7";
}
echo '<html>';
echo '<head>';
echo '  <meta http-equiv="Cache-Control" content="no-cache">';
echo '  <meta http-equiv="Pragma" content="no-cache">';
echo '  <meta http-equiv="Expires" content="0">';
echo '  <link rel="stylesheet" type="text/css" media="screen" href="/css/directory_list.css" />';
echo '  <link rel="icon" href="/images/pCP.png" type="image/x-icon" />';
echo '</head>';
echo '<body>';
echo '<!-- Start of pcp_banner -->';
echo '<table class="bgblack">';
echo '  <tr>';
echo '    <td height="148">';
echo '      <p class="banner">';
echo '        <img src="/images/banner.png" alt="piCorePlayer" />';
echo '      </p>';
echo '    </td>';
echo '  </tr>';
echo '</table>';
echo '<!-- End of pcp_banner -->';
echo '<div class="clear"></div>';
echo '    <h1>piCorePlayer Update Repository</h1>';
echo '    <h2>Index of ' . $curpath . '</h2>';
echo '    <div id="directory-list" class="list">';
echo '    <table summary="Directory Listing" cellpadding="0" cellspacing="0">';
echo '        <thead><tr>';
echo '        <th class="n">Name</th>';
echo '        <th class="m">Last Modified</th>';
echo '        <th class="s">Size</th>';
echo '        <th class="t">Type</th>';
echo '        </tr></thead>';
echo '    <tbody>';


$path = ".";
$dir = opendir($path);
$files = array();
while ($files[] = readdir($dir));
sort($files);
closedir($dir);

echo '  <tr>';
echo '    <td>';
echo '     <img src="/images/back.gif" alt="[DIR]" style="width:12px;height:12px;"><a href="' . $path . '/..">&#60;Parent Directory&#62;</a>';
echo '    </td>';
echo '  </tr>';
foreach ($files as $file){
	if ($file == "releases"){
		echo '  <tr>';
		echo '    <td class="n">';
		echo '      <img src="/images/folder.gif" alt="[DIR]" style="width:12px;height:12px;">';
		echo '      <a href=https://sourceforge.net/projects/picoreplayer/files/repo/8.x/' . $arm . '/releases/>releases</a>';
		echo '    </td>';
		echo '    <td class="m">';
        echo "      <p>" . date ("Y-M-d H:i:s", filemtime($file)) . "</p>";
		echo '    </td>';
		echo '    <td class="s">';
		echo '      <p>' . human_filesize(filesize($file), 1) .'</p>';
		echo '    </td>';
		echo '    <td class="t">';
		echo '      <p>' . filetype($file) .'</p>';
		echo '    </td>';
		echo '  </tr>';
	} else if($file != "" && $file != "." && $file != ".." && $file != "index.php" && $file != ".htaccess" && $file != "error_log" && $file != "cgi-bin" && $file != "create_repo_files" && $file != "repo.htm" ) {
		$ft = filetype($file);
		echo '  <tr>';
		echo '    <td class="n">';
		switch ($ft) {
			case "dir":
				echo '     <img src="/images/folder.gif" alt="[DIR]" style="width:12px;height:12px;">';
				break;
			case "file":
				echo '     <img src="/images/text.gif" alt="[txt]" style="width:12px;height:12px;">';
				break;
			default:
				echo '     <img src="/images/blank.gif" alt="[   ]" style="width:12px;height:12px;">';
		}
        echo "      <a href='$path/$file'>$file</a>";
		echo '    </td>';
		echo '    <td class="m">';
        echo "      <p>" . date ("Y-M-d H:i:s", filemtime($file)) . "</p>";
		echo '    </td>';
		echo '    <td class="s">';
		echo '      <p>' . human_filesize(filesize($file), 1) .'</p>';
		echo '    </td>';
		echo '    <td class="t">';
		echo '      <p>' . $ft .'</p>';
		echo '    </td>';
		echo '  </tr>';
    }
}
echo '</tbody>';
echo '</table>';
echo '</div>';
echo '</body>';
echo '</html>';
?> 
