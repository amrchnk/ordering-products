<template>
<main>
  <div class="wrap">
      <div class="text">
        <h1>Настройки</h1>
      </div>
      <div class="user_data">
        <div class="line">
          <div class="lbls">
            <label class="pre">Имя пользователя:</label>
            <label v-if="!editMode">{{this.full_name}}</label>
            <input type="text" v-if="editMode" v-model="user.full_name">
          </div>
          <a class="nav-link" href="#" v-if="!editMode" @click="includeEdit">Изменить</a>
        </div>
        <div class="line">
          <div class="lbls">
            <label class="pre">Электропочта:</label>
            <label v-if="!editMode">{{ this.email }}</label>
            <input type="text" v-if="editMode" v-model="user.email">
          </div>
          <a class="nav-link" href="#" v-if="!editMode" @click="includeEdit">Изменить</a>
        </div>
        <div class="line">
          <div class="lbls">
            <label class="pre">Пароль:</label>
            <label v-if="!editMode">{{this.password}}</label>
            <input type="text" v-if="editMode" v-model="user.password">
          </div>
          <a class="nav-link" href="#" v-if="!editMode" @click="includeEdit">Изменить</a>
        </div>
        <div class="line">
          <div class="lbls">
            <label class="pre">Номер телефона:</label>
            <label v-if="!editMode" class="num">{{this.phone_num}}</label>
            <input class="num" type="text" v-if="editMode" v-model="user.phone">
          </div>
          <a class="nav-link" href="#" v-if="!editMode" @click="includeEdit">Изменить</a>
        </div>
      </div>
      <button class="btn btn-primary" v-if="editMode" @click="Update">Сохранить</button>
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
main{
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
}
.wrap{
  width: 70%;
  background-color: white;
  border-radius: 15px;
  margin-top: 30px;
  padding: 40px;
}
h1{
  font-size: 2.7em;
  font-weight: bold;
}
input{
  margin-bottom: 15px;
}
.num{
  font-family: "Open Sans", sans-serif;
}
.line{
  display: flex;
  width: 25em;
  justify-content: space-between;
  margin-bottom: 15px;
}
label{
  font-size: 1.2em;
}
.pre{
  font-weight: 600;
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
.user_data{
  margin-top: 20px;
  width: 100%;
}
.lbls{
  display: flex;
  width: 16em;
  justify-content: space-between;
}

@media (max-width: 900px) {
  h1 {
    font-size: 2.5em;
  }
  .wrap{
    width: 80%;
  }
}

@media (max-width: 580px) {
  .wrap{
    padding: 40px 30px;
  }
  h1 {
    font-size: 2.3em;
  }
  .line{
    width: 100%;
  }
  .lbls{
    width: 15em;
    font-size: 0.9em;
  }
  .nav-link{
    font-size: 0.9em;
  }
}

@media (max-width: 490px) {
  .wrap{
    width: 100%;
    border-radius: 0px;
  }
}

@media (max-width: 390px) {
  .lbls{
    font-size: 0.8em;
    align-items: center;
  }
  .nav-link{
    font-size: 0.8em;
  }
  .line{
    align-items: center;
  }
}
</style>