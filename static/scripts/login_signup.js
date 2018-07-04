/**
 * Created by qimi on 2016/5/2.
 */


$(document).ready(function() {
   $("#input-form").find(":submit").click(function() {
       if ($.MyCheckValidity("#input-form")) {
           return true;
       } else {
           return false;
       }
   })
});