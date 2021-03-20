<template>
  <div class="home">
    <v-data-table
    :headers="headers"
    :items="items"
    dense
    style="width: 400px"
  >
  <template v-slot:top>
  <v-toolbar
        flat
      >
  <v-dialog
          v-model="dialog"
          max-width="500px"
        >
     <template v-slot:activator="{ on, attrs }">
            <v-btn
              color="primary"
              dark
              class="mb-2"
              v-bind="attrs"
              v-on="on"
            >
              New Account
            </v-btn>
          </template>
          <v-card>
            <v-card-title>
              <span class="headline">{{ formTitle }}</span>
            </v-card-title>

            <v-card-text>
              <v-container>
                <v-row>
                  <v-col
                    cols="12"
                    sm="6"
                    md="4"
                  >
                    <v-text-field
                      v-model="editedItem.Account"
                      label="Account name"
                    ></v-text-field>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>

            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn
                color="blue darken-1"
                text
                @click="close"
              >
                Cancel
              </v-btn>
              <v-btn
                color="blue darken-1"
                text
                @click="save"
              >
                Save
              </v-btn>
            </v-card-actions>
          </v-card>
          </v-dialog>
          <v-dialog v-model="dialogDelete" max-width="500px">
          <v-card>
            <v-card-title class="headline">Are you sure you want to delete this item?</v-card-title>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue darken-1" text @click="closeDelete">Cancel</v-btn>
              <v-btn color="blue darken-1" text @click="deleteItemConfirm">OK</v-btn>
              <v-spacer></v-spacer>
            </v-card-actions>
          </v-card>
        </v-dialog>
        </v-toolbar>
  </template>
  
  <template v-slot:item.actions="{ item }">
      <v-icon
        small
        class="mr-2"
        @click="editItem(item)"
      >
        mdi-pencil
      </v-icon>
      <v-icon
        small
        @click="deleteItem(item)"
      >
        mdi-delete
      </v-icon>
    </template>
    <template v-slot:no-data>
      <v-btn
        color="primary"
        @click="initialize"
      >
        Reset
      </v-btn>
    </template>
  </v-data-table>
  <v-overlay :value="overlay"><v-progress-circular v-if="overlay"
      indeterminate
    ></v-progress-circular></v-overlay>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  methods:{
  sync(){
    this.overlay = true;
    var myform = new FormData();
    myform.append("accounts",this.accounts);
    axios.post('/UpdateAccounts', myform).then(() =>{
      this.overlay=false;
    });
  },
  editItem (item) {
        this.editedIndex = this.accounts.indexOf(item.Account)
        this.editedItem = Object.assign({}, item)
        this.dialog = true
      },
     getAccounts(){
     this.overlay =true;
       axios.post('/GetAccounts').then((response) =>{
       this.overlay = false;
          this.accounts = response.data.accounts;
       });
     
     },
     deleteItem (item) {
        this.editedIndex = this.accounts.indexOf(item.Account)
        this.editedItem = Object.assign({}, item)
        this.dialogDelete = true
      },deleteItemConfirm () {
        this.accounts.splice(this.editedIndex, 1)
        this.sync();
        this.closeDelete()
      },close () {
        this.dialog = false
        this.$nextTick(() => {
          this.editedItem = Object.assign({}, this.defaultItem)
          this.editedIndex = -1
        })
      }, closeDelete () {
        this.dialogDelete = false
        this.$nextTick(() => {
          this.editedItem = Object.assign({}, this.defaultItem)
          this.editedIndex = -1
        })
      },save () {
        if (this.editedIndex > -1) {
        this.$set(this.accounts, this.editedIndex, this.editedItem.Account);
        } else {
          this.accounts.unshift(this.editedItem.Account)
        }
        this.sync();
        this.close()
      },
  },
    watch: {
      dialog (val) {
        val || this.close()
      },
      dialogDelete (val) {
        val || this.closeDelete()
      },
    },
  computed:{
  formTitle () {
        return this.editedIndex === -1 ? 'New Account' : 'Edit Account'
      },
    items(){
      var res = [];
      for(var i =0; i< this.accounts.length; i++)
         res.push({'Account': this.accounts[i]});
      return res;
    }
  },
  data() {
    return {
    dialog: false,
    dialogDelete: false,
    editedIndex: -1,
    editedItem: {'Account': ''},
    defaultItem: {'Account': ''},
      overlay: false,
      accounts:[],
      headers: [{text:'Account', value: 'Account'}, { text: 'Actions', value: 'actions', sortable: false }]
    }},
   mounted(){
     this.getAccounts();
   }
  
}
</script>
