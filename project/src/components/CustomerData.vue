<template>
  <main>
<!--    <div>-->
<!--      <PaySuccess v-if="visible && payed && !error" @closeModal="closeModal" ref="PaySuccess"/>-->
<!--      <PayError v-if="visible && !payed && error" @closeModal="closeModal" ref="PayError"/>-->
<!--    </div>-->

    <div class="wrap">
      <div class="breadcrumb">
        <router-link to="/basket" class="rl"><b>Корзина</b></router-link>
        <p class="slash">/</p>
        <p>Новый заказ</p>
      </div>
    </div>
    <div class="wrap">
      <div class="text">
        <h1>Новый заказ</h1>
      </div>
    </div>
    <div class="wrap">
      <div class="container">
        <div class="form">
          <form @submit.prevent :disabled="visible">
            <div class="customer">
              <h2>Заказчик</h2>
              <hr>
              <div class="strs">
                <div class="str">
                  <h5 class="marked">ФИО</h5>
                  <h5>{{ newOrder.full_name }}</h5>
                </div>
                <div class="str">
                  <h5 class="marked">Email</h5>
                  <h5>{{ newOrder.email }}</h5>
                </div>

                <div class="str">
                  <h5 class="marked">Телефон</h5>
                  <h5 class="num">{{ newOrder.phone }}</h5>
                </div>
              </div>

            </div>

            <div class="address">
              <h2>Адрес доставки</h2>
              <hr>
              <input :disabled="visible" type="text" class="form-control" id="address" placeholder="Введите ваш адрес" v-model="newOrder.to" required>
              <div class="ymap-container">
                <yandex-map
                    :coords="coords"
                    :zoom="10"
                    @click="onClick"
                >
                  <ymap-marker
                      :coords="coords"
                      marker-id="124"
                      hint-content="some hint"
                  />
                </yandex-map>
              </div>
            </div>

            <div class="custom-control custom-checkbox">
              <input :disabled="visible" type="checkbox" class="custom-control-input" id="finish-text" v-model="checkedConfirm">
              <label class="custom-control-label" for="finish-text">Я даю согласие на обработку персональных данных</label>
            </div>
            <button class="btn btn-success btn-block" :disabled="!checkedConfirm || visible" @click="saveNewOrder()">Оплатить заказ</button>
            <button class="btn btn-danger btn-block" :disabled="visible" @click="clearForm()">Очистить форму</button>
          </form>
        </div>
      </div>
    </div>
  </main>
</template>

<script>
import PaySuccess from './PaymentOrderSuccess.vue';
import PayError from './PaymentOrderError.vue';


  export default {
    name: "neworder",
    components: {
      PaySuccess,
      PayError
    },
    data() {
      return {
        coords:[55.753220, 37.622513],
        newOrder: {
          id_client: Number.parseInt(document.cookie.replace(/(?:(?:^|.*;\s*)id=\s*\s*([^;]*).*$)|^.*$/, "$1")),
          full_name: document.cookie.replace(/(?:(?:^|.*;\s*)full_name=\s*\s*([^;]*).*$)|^.*$/, "$1"),
          email: document.cookie.replace(/(?:(?:^|.*;\s*)email=\s*\s*([^;]*).*$)|^.*$/, "$1"),
          phone: document.cookie.replace(/(?:(?:^|.*;\s*)phone_num=\s*\s*([^;]*).*$)|^.*$/, "$1"),
          to: "",
          cost: 0,
          id_cart: null
        },
        checkedConfirm: false,
        visible: false,
        payed: false,
        error: false,
        address: "http://localhost:5002",
        address_orders: "http://localhost:5001", //drop later
      }
    },
    methods: {
      async onClick(e) {
        this.coords = e.get('coords');
		    await ymaps.geocode(this.coords).then((res) => (this.newOrder.to = res.geoObjects.get(0).properties.get('text')));
      },
      async getCart() {
        try {
          let request = {
            "jsonrpc": "2.0",
            "method": "App.get_cart",
            "params": {
              "id_client": this.newOrder.id_client
            },
            "id": 1
          }
          let response = "";
          await this.$http.post(`${this.address}/carts`, request)
            .then((res) => res.json()).then((res) => (response = res.result));
          if (response['error'] == '') {
            this.newOrder.id_cart = response['id']
            this.newOrder.cost = response['cost']
          }
        }
        catch (e) {
          console.log(e)
          alert("Сервер недоступен, попробуйте позже");
        }
      },
      saveNewOrder() {
        if (this.newOrder.id_client != "" && this.newOrder.full_name != "" && this.newOrder.email != ""&& this.newOrder.phone != "" &&
        this.newOrder.to != "" && this.newOrder.cost != 0 && this.newOrder.id_cart != null) {
          this.addNewOrder();
          this.clearForm();
          this.$router.push('/paymentLoad');
        }
      },
      async addNewOrder() {
        try {
          let request = {
            "jsonrpc": "2.0",
            "method": "App.add_order",
            "params": {
              "id_cart": this.newOrder.id_cart,
              "id_client": this.newOrder.id_client,
              "cost": this.newOrder.cost,
              "address": this.newOrder.to
            },
            "id": 1
          }
          await this.$http.post(`${this.address_orders}/orders`, request)
            .then((res) => res.json()).then((res) => {
              alert("Ваш заказ - № " + res.result);
              console.log(res)
              this.deleteCart();
            });
        }
        catch(err) {
          console.error(err);
        }
      },
      async deleteCart() {
        try {
          let request = { //тело запроса на бэк
            "jsonrpc": "2.0",
            "method": "App.delete_cart",
            "params": {
              "id_cart": this.newOrder.id_cart
            },
            "id": 1
          }
          let response = "";
          await this.$http.post(`${this.address}/carts`, request)
            .then((res) => res.json()).then((res) => (response = res.result));
          if (response != "success") {
            alert("Произошла ошибка, повторите операцию")
          }
        }
        catch (e) {
          console.log(e);
          alert("Сервер недоступен, попробуйте позже");
        }
      },
      clearForm() {
        this.newOrder.to = ""
      }
    },
    async created() {
      await this.getCart();
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
  display: flex;
  justify-content: center;
  align-items: center;
}
.text{
  width: 100%;
  margin-top: 5px;
}
h1{
  font-size: 3.4em;
  font-weight: bold;
}
.container{
  display: flex;
  width: 100%;
  padding: 0;
  margin-top: 10px;
  background-color: white;
  border-radius: 15px;
  padding: 40px;
}
h2{
  font-weight: 400;
  font-size: 1.7em;
}
.address{
  margin-top: 40px;
}
.form,.address{
  width: 100%;
}
input{
  margin-top: 30px;
}

.custom-control-label{
  margin-left: 10px;
}
.btn{
  margin-top: 15px;
}
.btn-danger{
  margin-left: 10px;
}
.strs{
  display: flex;
  flex-direction: column;
  width: 15em;
}
.str{
  display: flex;
  justify-content: space-between;
  margin: 0;
  margin-top: 10px;
}
.marked{
  font-weight: 600;
}
.ymap-container{
  margin-top: 20px;
  width: 100%!important;
}
.breadcrumb{
  width: 100%;
  margin-top: 50px;
  display: flex;
  justify-content: left;
  margin-bottom: 0;
}
p{
  margin:0;
}
.rl{
  text-decoration: none;
  color: inherit;
}
.slash{
  margin: 0 10px;
}
b{
  color: #4e4e4e;
  font-weight: 600;
}
.num{
  font-family: 'Open Sans', sans-serif;
  font-weight: 400;
}
</style>
