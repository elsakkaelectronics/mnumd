<?php
$mod = $_COOKIE['mod'];$type=$_COOKIE['type'] ; $path= "./".$mod.'/'.$type.'lst.txt';$lstjon = fopen('./leclst.json' , 'w');
$raw = fopen($path , 'r');
fwrite($lstjon ,file_get_contents($path) .']'   ); #echo(file_get_contents($path) . $path );
 $leclst= json_decode(file_get_contents('./leclst.json'));
print_r($leclst);echo("<div style='display:flex;flex-direction:column;background-color:rgb(242 242 242);height:calc(100vh - 100px);
   '>");
foreach ($leclst as $lec){
   echo(       "
    <form method='post'><a > <input type='submit' value=$lec->name name=".$lec->name .">" ."</a>
   
    <input type='hidden' name='lec' value='$lec->path'>
   
   
   "
   );     
};
echo("</div><style>
a{
  flex:1;
  background:rgb(225 227 232);
margin-top:6px;
text-align:center;
justify-content:center;
display:flex;}
a input{
  align-self:center;
font-size: 6vw;height:100%;background-color:transparent;border:0px
}
form{
    display:flex;
    flex-direction:column;flex:1;
    ");