<template>
	<main>
		<h2 class="h2">Для совершения заказов на нашем сайте, вам необходимо войти в систему</h2>
    <div class="wrap">
      <div class="form_wrap">
        <div class="form">
          <div class="fields">
            <div class="field">
              <label class="form-label">Логин</label>
              <input class="form-control" id="exampleInputEmail1" v-model="user.email">
            </div>

            <div class="field">
              <label class="form-label">Пароль</label>
              <input class="form-control" id="exampleInputPassword" v-model="user.password" type="password">
            </div>
            <div class="others">
              <button class="btn btn-primary" @click="login">Войти</button>
              <router-link class="rl link" to="/reg">У меня нет аккаунта</router-link>
            </div>

            <div class="field social">
              <label class="form-label">Войти с помощью</label>
              <div class="social-inner">
                <button class="ico vk" @click="ShowMSG">
                  <img class="imic" src="@/assets/vk.svg">
                </button>
                <button class="ico fb">
                  <img class="imich" src="@/assets/fb.svg">
                </button>
                <button class="ico od">
                  <img class="imich" src="@/assets/ok.svg">
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

	</main>

</template>

<script>
export default {
  name: "Autho",
  data() {
    return {
      version: "1.0",
      address: "http://localhost:5000",
      user: {
        id: '',
        full_name: '',
        email: '',
        password:'',
        phone: '',
        error:''
      }
    }
  },
  components: {},
  methods: {
    ShowMSG(){
      alert(this.email)
    },
    async login() { // По нажатию на кнопку "Войти"
      if (this.user.email.length > 0 && this.user.password.length > 0) {// Проверяем, чтобы поля логина и пароля не были пустыми
        try {
          let request = { //тело запроса на бэк
            "jsonrpc": "2.0",
            "method": "App.login_user",
            "params": { "email": this.user.email,"password":this.user.password },
            "id": 1
          }
          await this.$http.post(`${this.address}/clients`, request) //по JSON RPC запросы идут только через POST
              .then((res) => res.json()).then((res) => (this.user = res.result)); //ответ берем обязательно из res.result
          console.log(this.user);
          if (this.user.error =='') {
            document.cookie = `id=${this.user.id}`;
            document.cookie = `email=${this.user.email}`;
            document.cookie = `password=${this.user.password}`;
            document.cookie = `full_name=${this.user.full_name}`;
            document.cookie = `phone_num=${this.user.phone}`;
            await this.$router.push('/');
          } else {
            alert(this.user.error);
          }
        } catch (e) {
          console.log(e);
          alert("Сервер недоступен, попробуйте позже");
        }
      } else
        alert("Поля email и password не могут быть пустыми");
    }
  },
  async created() {
    // При открытии смотрим куки. При наличии логина и пароля - пытаемся авторизоваться
    let email = document.cookie.replace(/(?:(?:^|.*;\s*)email=\s*\s*([^;]*).*$)|^.*$/, "$1");
    let password = document.cookie.replace(/(?:(?:^|.*;\s*)password=\s*([^;]*).*$)|^.*$/, "$1");
    if (email !== "" && password !== "")
      await this.$router.push('/userPage');
  }
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
	display: flex !important;
	align-items: center!important;
	justify-content: space-between;
	margin-bottom: 20px;
}
.link{
	text-decoration: none;
	margin-left: 20px;
}

.social{
  margin-bottom: 10px!important;
}

.vk{
	background-color: #2787F5;
}

.od{
	background-color: #F78306;
}

.fb{
	background-color: #4867AA;
}

.rl{
  color: #2787F5 !important;
}

.ico{
	width: 50px;
	height: 50px;
	border: none;
}
.imic{
	width: 30px;
}

.imich{
	height: 30px;
}

.social-inner{
	display: flex;
	align-items: center;
}

@media (max-width: 1350px) {
  .wrap {
    width: 32em;
  }
  .fields{
    padding: 30px 50px
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

@media (max-width: 770px) {
  h2{
    width: 70%;
  }
}

@media (max-width: 580px) {
  h2{
    width: 80%;
  }
  .wrap {
    width: 26em;
  }
  .fields{
    padding: 30px 40px
  }
  .ico{
    width: 40px;
    height: 40px;
  }
  .imic{
    width: 20px;
  }

  .imich{
    height: 20px;
  }
}

@media (max-width: 460px) {
  h2{
   font-size: 1em;
  }
  .wrap {
    width: 24em;
  }
  .btn,.others{
    font-size: 0.9em;
  }
}
@media (max-width: 400px) {
  h2{
    width: 90%;
  }
  .wrap{
    width: 100%;
  }
  .form{
    border-radius: 0px;
  }
  .fields{
    padding: 20px 30px
  }
}
</style>
