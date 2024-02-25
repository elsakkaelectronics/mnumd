<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body style="height:100vh">
  <?php  
  include './header.php';
  $mod = "";if($_COOKIE['mod'] != null){
    $mod = $_COOKIE['mod'];
  }
  print_r($_COOKIE);

  if ($mod == ""){
    header('location: choosemod.php');
    print_r($mod);
  };

  echo("
  <div style='display:flex;flex-direction:column;background-color:rgb(242 242 242);height:calc(100vh - 100px);
  '> <a > <p> sign in</p></a>
  <a ><p> الكويزات</p></a>
  <a ><p> ملخصات</p></a>
  <a ><p> الشرح</p></a>
  <a><p> forum</p></a>
  <a ><p> support</p></a>
  <a> <p> researches </p> </a>
  <a ><p> ekp </p></a>
  <a ><p> ibn el haitham</p></a>
  </div>
  <style>
  a{
    flex:1;
    background:rgb(225 227 232);
  margin-top:6px;
  text-align:center;
  justify-content:center;
  display:flex;}
  a p{
    align-self:center;
  font-size: 6vw;
  }
  ");