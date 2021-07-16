<template>
  <div>
    <div>
      <PaySuccess v-if="visible && payed && !error" @closeModal="closeModal" ref="PaySuccess"/>
      <PayError v-if="visible && !payed && error" @closeModal="closeModal" ref="PayError"/>
    </div>
    <div class="col-md-8 mx-auto">
      <nav aria-label="breadcrumb" class="wrap-in">
        <ol class="breadcrumb">
          <li class="breadcrumb-item base"><router-link to="/basket">Корзина</router-link></li>
          <li class="breadcrumb-item cur">Оплата</li>
        </ol>
      </nav>
    </div>
    <h1 class="text-center">Новый заказ</h1>

    <div class="row mx-0">

      <div class="col-md-8 mx-auto">

        <form @submit.prevent :disabled="visible">
          <h2>Заказчик</h2>
          <div class="row">
            <div class="col-md-6 str" >
              <h5>ФИО</h5>
              <h5 class="dop">{{ newOrder.full_name }}</h5>
            </div>
            <div class="col-md-6 str">
              <h5>Email</h5>
              <h5 class="dop">{{ newOrder.email }}</h5>
            </div>

            <div class="col-md-6 str">
              <h5>Телефон</h5>
              <h5 class="dop">{{ newOrder.phone }}</h5>
            </div>
          </div>

          <hr class="mb-4">

          <h2>Адрес доставки</h2>
          <div class="mb-3 mt-3 form-group">
            <input :disabled="visible" type="text" class="form-control" id="address" placeholder="Введите ваш адрес" v-model="newOrder.to" required>
          </div>
          <div>
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

          <hr class="mb-4">
          <div class="custom-control custom-checkbox mb-4">
            <input :disabled="visible" type="checkbox" class="custom-control-input" id="finish-text" v-model="checkedConfirm">
            <label class="custom-control-label" for="finish-text" style="font-size: 1rem;">Я даю согласие на обработку персональных данных</label>
          </div>
          <button class="btn btn-success btn-lg btn-block" :disabled="!checkedConfirm || visible" @click="saveNewOrder()">Оплатить заказ</button>
          <button class="btn btn-danger btn-lg btn-block" :disabled="visible" @click="clearForm()">Очистить форму</button>
        </form>

      </div>

    </div>
  </div>
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
.str{
  display: flex;
  justify-content: left;
}
.dop{
  margin-left: 30px;
}
h1{
  margin-top: 20px;
}
h2{
  font-weight: 600;
}
.cur{
  font-weight: 600;
}
button{
  margin-bottom: 50px !important;
}

</style>
