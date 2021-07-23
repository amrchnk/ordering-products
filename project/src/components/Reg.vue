<template>
	<main>
		<h2 class="h2">Чтобы зарегистрироваться в системе, укажите следующие данные</h2>
    <div class="wrap">
      <div class="form_wrap">
        <div class="form">
          <div class="fields">
            <div class="field">
              <label class="form-label">ФИО</label>
              <input class="form-control" id="exampleInputEmail1" v-model="user.full_name">
            </div>

            <div class="field">
              <label class="form-label">Адрес вашей электронной почты</label>
              <input class="form-control" id="exampleInputEmail1" v-model="user.email">
            </div>

            <div class="field">
              <label class="form-label">Пароль</label>
              <input class="form-control" id="exampleInputEmail1" v-model="user.password" type="password">
            </div>

            <div class="field">
              <label class="form-label">Телефон</label>
              <input class="form-control" id="exampleInputEmail1" v-model="user.phone_num">
            </div>

            <div class="field check_field">
              <input type="checkbox" class="form-check-input">
              <label class="form-label rules">Я принимаю условия пользовательского соглашения</label>
            </div>

            <div class="others">
              <button class="btn btn-primary" @click="reg">Зарегистрироваться</button>
              <router-link class="link" to="/autho">Назад к авторизации</router-link>
            </div>

          </div>
        </div>
      </div>
    </div>


	</main>
</template>

<script>
export default {
  name: "Reg",
  data() {
    return {
      version: "1.0",
      address: "http://localhost:5000",
      user: {
        full_name: "",
        email: "",
        password: "",
        phone_num: ""
      },
      answer: {}
    }
  },
  methods: {
    async reg() { // По нажатию на кнопку "Войти"
      if (this.user.full_name.length > 0 && this.user.email.length > 0 && this.user.phone_num.length > 0 && this.user.password.length > 0) {// Проверяем, чтобы поля логина и пароля не были пустыми
        try {
          let request = { //тело запроса на бэк
            "jsonrpc": "2.0",
            "method": "App.reg_user",
            "params": {"full_name": this.user.full_name, "email": this.user.email, "password": this.user.password, "phone": this.user.phone_num },
            "id": 1
          }
          await this.$http.post(`${this.address}/clients`, request) //по JSON RPC запросы идут только через POST
              .then((res) => res.json()).then((res) => (this.answer = res.result)); //ответ берем обязательно из res.result
          console.log(this.user);
          if (this.answer =='success') {
            alert('Вы успешно зарегистрированы!')
            await this.$router.push('/autho');
          } else if(this.answer=='error'){
            alert('Пользователь с таким логином или номером телефона уже зарегистрирован');
          }
        } catch (e) {
          console.log(e);
          alert("Сервер недоступен, попробуйте позже");
        }
      } else
        alert("Поля не могут быть пустыми");
    }
  },
}
</script>

<style scoped>
main{
  display: flex;
  flex-direction: column;
  align-items: center;
}
.wrap{
  width: 34em;
  display: flex;
  justify-content: center;
  align-items: center;
}
h2{
  margin-top: 50px;
  font-weight: 400;
  text-align: center;
  font-size: 1.5em;
}
.form_wrap{
  width: 100%;
}
.form{
  background-color: white;
  border-radius: 10px;
  border: 0.5px solid #E5E5E5;
  margin-top: 30px;
}

.fields{
  padding: 35px 60px
}
.field{
  width:100%; 
  margin-bottom: 25px;
      clear:both; 
      text-align:left;

}
.others{
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.link{
  text-decoration: none;
  margin-left: 20px;
  color: #2787f5;
}

.rules{
  margin-bottom: 0;
  margin-left: 10px;
  font-size: 1em;
}
.form-check-input{
  margin: 0;
  display: block;
}
.check_field{
  display: flex;
  align-items: center;
  width: 100%;
}
@media (max-width: 1350px) {
  .wrap {
    width: 30em;
  }
  .rules{
    font-size: 0.85em;
  }
  .fields{
    padding: 30px 50px
  }
  .others{
    margin-bottom: 0px;
  }
}

@media (max-width: 1100px) {
  .field,input{
    font-size: 0.9em;
  }
  h2{
    margin-bottom: 0;
    font-size: 1.2em;
  }
}
@media (max-width: 710px) {
  h2{
    padding: 0 90px;
  }
  .wrap {
    width: 28em;
  }
  .btn,.link{
    font-size: 0.9em;
  }
  .fields{
    padding: 30px 40px
  }
  .rules{
    font-size: 0.9em;
  }

}

@media (max-width: 540px) {
  h2{
    padding: 0 50px;
  }
  .wrap {
    width: 24em;
  }
  .fields{
    padding: 30px;
  }
  .btn,.link{
    font-size: 0.8em;
  }
  .field,input{
     font-size: 0.8em;
   }
}

@media (max-width: 450px) {
  h2{
    padding: 0 30px;
    font-size: 1em;
  }
  .wrap {
    width: 22em;
  }
  .fields{
    padding: 30px 25px;
  }
  .form-check-input{
    width: 9px;
    height: 9px;
  }
  .rules{
    margin-left: 8px;
  }
}

@media (max-width: 400px) {
  h2{
    padding: 0 10px;
    font-size: 0.9em;
  }
  .wrap{
    width: 100%;
  }
  .form{
    border-radius: 0px;
  }
}

</style>