<template>
  <div class="d-flex flex-column justify-content-center align-items-center">
    <h2>Перенаправление в онлайн-банк</h2>
    <h5>Пожалуйста, подождите...</h5>
  </div>
</template>

<script>
export default {
  name: "paymentLoad",
  data() {
    return {
      order: {
        id: "",
        id_client: "",
        cost: 0,
        status: "",
        address: ""
      },
      id_payment: "",
      address_orders: "http://localhost:5001", //drop later
      address_pay: "http://localhost:5004",
    }
  },
  methods: {
    async getUnpaidOrder() {
      try {
        let request = { //тело запроса на бэк
          "jsonrpc": "2.0",
          "method": "App.get_unpaid_order",
          "params": {
            "id_client": Number.parseInt(document.cookie.replace(/(?:(?:^|.*;\s*)id=\s*\s*([^;]*).*$)|^.*$/, "$1"))
          },
          "id": 1
        }
        await this.$http.post(`${this.address_orders}/orders`, request)
          .then((res) => res.json()).then((res) => (this.order = res.result));
        console.log(this.order)
      }
      catch (e) {
        console.log(e);
        alert("Сервер недоступен, попробуйте позже");
      }
    },
    async addPayment() {
      try {
        let request = { //тело запроса на бэк
          "jsonrpc": "2.0",
          "method": "App.add_payment",
          "params": {
            "id_order": this.order.id,
            "cost": this.order.cost
          },
          "id": 1
        }
        await this.$http.post(`${this.address_pay}/payments`, request)
          .then((res) => res.json()).then((res) => (this.id_payment = res.result));
        if (this.id_payment != "Server problem") {
          alert("Ваш заказ успешно оплачен")
          this.$router.push("/")
        }
        else {
          alert("Не удалось оплатить заказ")
          this.$router.push("/")
        }
      }
      catch (e) {
        console.log(e);
        alert("Сервер недоступен, попробуйте позже");
      }
    }
  },
  async created() {
    await this.getUnpaidOrder();
    await this.addPayment();
  }
}

</script>
