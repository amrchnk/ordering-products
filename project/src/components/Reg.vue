<template>
	<div class="main">
		<h2 class="reg-h2">Чтобы зарегистрироваться в системе, укажите следующие данные</h2>
		<div class="reg-form">
			<div class="reg-fields">
        <div class="reg-field">
          <label class="form-label">ФИО</label>
          <input class="form-control" id="exampleInputEmail1" v-model="user.full_name">
        </div>

        <div class="reg-field">
          <label class="form-label">Адрес вашей электронной почты</label>
          <input class="form-control" id="exampleInputEmail1" v-model="user.email">
        </div>

				<div class="reg-field">
					<label class="form-label">Пароль</label>
					<input class="form-control" id="exampleInputEmail1" v-model="user.password" type="password">
				</div>

        <div class="reg-field">
          <label class="form-label">Телефон</label>
          <input class="form-control" id="exampleInputEmail1" v-model="user.phone_num">
        </div>

				<div class="reg-field">
					<input type="checkbox" class="form-check-input" id="exampleInputEmail1">
					<label class="form-label rules">Я принимаю условия пользовательского соглашения</label>
				</div>



				<div class="reg-others">
					<button class="btn btn-primary" @click="reg">Зарегистрироваться</button>
					<router-link class="link rl" to="/autho">Назад к авторизации</router-link>
				</div>
				
			</div>
		</div>
	</div>
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

<style>
.reg-h2{
  margin-top: 70px;
  font-weight: 400;
  text-align: center;
  font-size: 1.5em;
  margin-bottom:20px;
}

.reg-form{
  background-color: white;
  width: 30%;
  border-radius: 10px;
  border: 0.5px solid #E5E5E5;
  margin: auto auto !important;
}

.main{
align-items: center;
}

.reg-fields{
  padding: 35px 60px
}
.reg-field{
  width:100%; 
  margin-bottom: 25px;
      clear:both; 
      text-align:left;

}
.reg-others{
  display: flex !important;
  align-items: center!important;
  justify-content: space-between;
  margin-bottom: 25px;
}
.reg-link{
  text-decoration: none;
  margin-left: 20px;
}

.rules{
  margin-left: 10px;
  font-size: 1em;
}

</style>