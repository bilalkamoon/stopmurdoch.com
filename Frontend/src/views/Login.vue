<template>
  <div class="login">
    <div>
      <form @submit.prevent="submit">
        <div>
          <label for="username">Username:</label>
          <input type="text" name="username" v-model="form.username" />
        </div>
        <div>
          <label for="password">Password:</label>
          <input type="password" name="password" v-model="form.password" />
        </div>
        <button type="submit">Submit</button>
      </form>
      <p v-if="error" id="error">{{error}}</p>
    </div>
    <div style="display: flex;justify-content: space-around;padding: 20px;"><a href="https://chaser.com.au/cancel-your-news-corp-subscription/" ><img src="/Cancel your Newscorp.png"></a><a href="https://chrome.google.com/webstore/detail/bye-rupert/ehdikikkfbfjjemfadgggcohkjoggoof?hl=en"><div style="width:583px;"><img src="/Bye%20Rupert.png"></div></a></div>
    <div><a href="https://unfoxmycablebox.com/">
    <img src="/Unfox.png" /></a></div>
    <div class="gfm-embed" data-url="https://www.gofundme.com/f/stop-murdoch/widget/large/"></div>
    <v-overlay :value="overlay"><v-progress-circular v-if="overlay"
      indeterminate
    ></v-progress-circular></v-overlay>
  </div>
</template>
<script>
import { mapActions } from "vuex";
import store from '../store';
export default {
  name: "Login",
  components: {},
  data() {
    return {
      form: {
        username: "",
        password: "",
      },
      error: "",
      overlay: false
    };
  },
  methods: {
    ...mapActions(["LogIn"]),
    async submit() {
      const User = new FormData();
      User.append("username", this.form.username);
      User.append("password", this.form.password);
      try {
      this.overlay = true;
          await this.LogIn(User);
          this.overlay = false;
          if(store.state.auth.user != null)
	          this.$router.push("/");
	   else{
	         this.error = store.state.auth.loginError;
      	   }
      } catch (error) {
        this.error = error
      } finally{
         this.overlay = false;
      } 
    },
  },
};
!function(t,e){try{function n(t){var n=e.createElement("iframe");return n.setAttribute("class","gfm-embed-iframe"),n.setAttribute("width","100%"),n.setAttribute("height","540"),n.setAttribute("frameborder","0"),n.setAttribute("scrolling","no"),n.setAttribute("src",t),n}t.addEventListener("message",function(t){t.data&&((function(t){return[].slice.call(e.getElementsByClassName("gfm-embed-iframe")).filter(function(e){return e.contentWindow===t.source})[0]}(t)).height=t.data.offsetHeight)},!1),e.addEventListener("DOMContentLoaded",function(){for(var t=e.getElementsByClassName("gfm-embed"),r=0;r<t.length;r++){var i=n(t[r].getAttribute("data-url"));t[r].appendChild(i)}})}catch(t){}}(window,document);
</script>
<style scoped>
* {
  box-sizing: border-box;
}
label {
  padding: 12px 12px 12px 0;
  display: inline-block;
}
button[type=submit] {
  background-color: #4CAF50;
  color: white;
  padding: 12px 20px;
  cursor: pointer;
  border-radius:30px;
}
button[type=submit]:hover {
  background-color: #45a049;
}
input {
  margin: 5px;
  box-shadow:0 0 15px 4px rgba(0,0,0,0.06);
  padding:10px;
  border-radius:30px;
}
#error {
  color: red;
}
</style>

