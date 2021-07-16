<template>
<main>
  <div class="wrap">
    <div class="wrap_body">
      <div class="text">
        <h1>Настройки</h1>
      </div>
      <div class="user_data">
        <div class="line">
          <label class="pre">Имя пользователя:</label>
          <label v-if="!editMode">{{this.full_name}}</label>
          <input type="text" v-if="editMode" v-model="user.full_name">
          <a class="nav-link" href="#" v-if="!editMode" @click="includeEdit">Изменить</a>
        </div>
        <div class="line">
          <label class="pre">Электропочта:</label>
          <label v-if="!editMode">{{ this.email }}</label>
          <input type="text" v-if="editMode" v-model="user.email">
          <a class="nav-link" href="#" v-if="!editMode" @click="includeEdit">Изменить</a>
        </div>
        <div class="line">
          <label class="pre">Пароль:</label>
          <label v-if="!editMode">{{this.password}}</label>
          <input type="text" v-if="editMode" v-model="user.password">
          <a class="nav-link" href="#" v-if="!editMode" @click="includeEdit">Изменить</a>
        </div>
        <div class="line">
          <label class="pre">Номер телефона:</label>
          <label v-if="!editMode">{{this.phone_num}}</label>
          <input type="text" v-if="editMode" v-model="user.phone">
          <a class="nav-link" href="#" v-if="!editMode" @click="includeEdit">Изменить</a>
        </div>
      </div>
      <button class="btn btn-primary" v-if="editMode" @click="Update">Сохранить</button>
    </div>
  </div>
</main>
</template>

<script>
export default {
name: "UserProfile",
  data(){
    return{
      id:parseInt(document.cookie.replace(/(?:(?:^|.*;\s*)id=\s*\s*([^;]*).*$)|^.*$/, "$1")),
      email: document.cookie.replace(/(?:(?:^|.*;\s*)email=\s*\s*([^;]*).*$)|^.*$/, "$1"),
      password: document.cookie.replace(/(?:(?:^|.*;\s*)password=\s*\s*([^;]*).*$)|^.*$/, "$1"),
      full_name: document.cookie.replace(/(?:(?:^|.*;\s*)full_name=\s*\s*([^;]*).*$)|^.*$/, "$1"),
      phone_num: document.cookie.replace(/(?:(?:^|.*;\s*)phone_num=\s*\s*([^;]*).*$)|^.*$/, "$1"),
      user:{
        email:'',
        password: '',
        full_name:'',
        phone:''
      },
      answer:'',
      version: "1.0",
      address: "http://localhost:5000",
      editMode:false
    }
  },
  methods:{
  includeEdit(){
    this.editMode=!this.editMode;
  },
  async Update(){
    alert(this.user.email)
    if (this.user.email.length > 0 && this.user.password.length > 0 && this.user.phone.length>0 && this.user.full_name.length>0) {// Проверяем, чтобы поля логина и пароля не были пустыми
      try {
        console.log(this.user,this.id);
        let request = { //тело запроса на бэк
          "jsonrpc": "2.0",
          "method": "App.change_user_data",
          "params": { "id_user": this.id,"full_name": this.user.full_name, "email": this.user.email, "password": this.user.password, "phone": this.user.phone},
          "id": 1
        }
        await this.$http.post(`${this.address}/clients`, request) //по JSON RPC запросы идут только через POST
            .then((res) => res.json()).then((res) => (this.answer = res.result)); //ответ берем обязательно из res.result

        if (this.answer =='success') {
          alert('Данные успешно изменены!')
          document.cookie = `id=${this.id}`;
          document.cookie = `email=${this.user.email}`;
          document.cookie = `password=${this.user.password}`;
          document.cookie = `full_name=${this.user.full_name}`;
          document.cookie = `phone_num=${this.user.phone}`;
        } else {
          alert(this.answer);
        }
      } catch (e) {
        console.log(e);
        alert("Сервер недоступен, попробуйте позже");
      }
      this.editMode=false;
    } else
      alert("Поля не могут быть пустыми!");
  }
  },
  mounted() {
  this.user.email=this.email;
  this.user.password=this.password;
  this.user.full_name=this.full_name;
  this.user.phone=this.phone_num;
  }
}
</script>

<style scoped>
.wrap_body{
  width: 80%;
  background-color: white;
  border-radius: 15px;
  margin-top: 30px;
  padding: 50px 60px 45px;
}
input{
  margin-bottom: 15px;
}
.user_data{
  font-family: "Open Sans", sans-serif;
  margin-top: 20px;
}
.line{
  display: flex;
}
label{
  font-size: 1.2em;
  margin-bottom: 15px;
}
.pre{
  font-weight: 600;
  margin-right: 20px;
}
button{
  width: 180px;
  font-size: 1.2em;
  margin-top: 15px;
}
a{
  margin:0;
  padding: 0;
  margin-left: 30px;
  color: #2787F5;
}
</style>