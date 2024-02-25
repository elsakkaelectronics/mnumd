<?php include './header.php';
echo(" <div> <form action='' method='post' enctype='multipart/form-data'><input name='file' type='file'> <input name='name'> <input name='path'>
<input list='type' name='type'>
<datalist id='type'>
<option value='lec'> 
<option value='prac '> 

</datalist>
<input type='submit' > </form></div>
");
$lst = fopen("./".$_POST["path"].'/'.$_POST['type'].'lst.txt','a');
if($_SERVER['REQUEST_METHOD'] == 'post'){
        print_r($_FILES);
};#print_r($_FILES );
move_uploaded_file($_FILES['file']['tmp_name'] , './'  . $_POST['path'] .'/' . $_FILES['file']['name']);print_r($_FILES['file']['name']);
$path = './'  . $_POST['path'] .'/' . $_FILES['file']['name'];
fwrite($lst , ',{"type":"'.$_POST['type'].
    '", "name":"'.$_POST['name'].
    '","path":'.'"'.$path.
'"}'); 