<?php include './header.php';
setcookie('mod' , 1);
echo("
<div style='display:flex;flex-direction:column;background-color:rgb(242 242 242);height:calc(100vh - 100px);
'> 
<a ><input type='button' value= ' f1' 
onclick='document.cookie = `mod =f1` ;window.location.replace(`index.php`)'></a>
<a ><input type='button' value= ' f2' 
onclick='document.cookie = `mod =f2` ;window.location.replace(`index.php`)'></a>
<a ><input type='button' value= ' f3' 
onclick='document.cookie = `mod =f3` ;window.location.replace(`index.php`)'></a>
<a><input type='button' value= ' f4' 
onclick='document.cookie = `mod =f4` ;window.location.replace(`index.php`)'></a>
<a ><input type='button' value= ' musk1' 
onclick='document.cookie = `mod =musk1` ;window.location.replace(`index.php`)'></a>
<a> <input type='button' value= ' musk2' 
onclick='document.cookie = `mod =musk2` ;window.location.replace(`index.php`)'> </a>
<a > <input type='button' value= ' blood and lymph' 
onclick='document.cookie = `mod =blood&lymph` ;window.location.replace(`index.php`)'></a>
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
div input{
    align-self:center;
font-size: 6vw;
width:60vw;
height:100%}
  .headerinput input {
    visibility: collapse}

");