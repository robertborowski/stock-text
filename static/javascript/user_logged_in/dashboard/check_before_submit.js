var wasSubmitted = false;    
function checkBeforeSubmit(){
  if(!wasSubmitted) {
    wasSubmitted = true;
    return wasSubmitted;
  }
  return false;
}