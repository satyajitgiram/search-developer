let form = document.getElementById('login-form');
console.log(form)

form.addEventListener('submit',(e)=>{
    e.preventDefault();
    console.log('Form Submitted')
    let formdata = {
        'username': form.username.value,
        'password': form.password.value
    }

    fetch('http://localhost:8000/api/users/token/',{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body:JSON.stringify(formdata)
    })
    .then(response => response.json())
    .then(data =>{
        console.log('Success', data)
        if (data.access){
            localStorage.setItem('token', data.access)
            window.location = 'index.html'
        }
        else{
            alert('Invalid Credentials')
        }
    })
    console.log(formdata)
})