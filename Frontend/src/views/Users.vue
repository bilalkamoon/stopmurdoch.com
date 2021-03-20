<template>
  <div class="home">
    <v-data-table
    :headers="headers"
    :items="items"
    dense
    style="width: 600px"
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
              New User
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
                      v-model="editedItem.Username"
                      label="Username"
                    ></v-text-field>
                    <v-text-field
                      v-model="editedItem.Password"
                      label="Password"
                    ></v-text-field>
                    <v-switch
                       v-model="editedItem.isAdmin"
                       label="isAdmin"></v-switch>
                    <v-text-field
                      v-model="editedItem.Email"
                      label="Email"
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
            <v-card-title class="headline">Are you sure you want to delete this user?</v-card-title>
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
    <!--
    <template v-slot:no-data>
      <v-btn
        color="primary"
        @click="initialize"
      >
        Reset
      </v-btn>
    </template>
    -->
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
  editItem (item) {
        this.items.forEach((i, idx) => {if(item.Username == i.Username) this.editedIndex = idx;});
        this.editedItem = Object.assign({}, item)
        this.editedItem['OldUsername'] = this.editedItem.Username;
        this.dialog = true
      },
     getUsers(){
     this.overlay =true;
       axios.post('/GetUsers').then((response) =>{
       this.overlay = false;
          this.items = response.data.users;
       });
     
     },
     deleteItem (item) {
        this.items.forEach((i, idx) => {if(item.Username == i.Username) this.editedIndex = idx;});
        this.editedItem = Object.assign({}, item)
        this.dialogDelete = true
      },deleteItemConfirm () {
        this.items.splice(this.editedIndex, 1)
        var myform = new FormData();
	    myform.append("username",this.editedItem.Username);
	    axios.post('/DeleteUser', myform).then(() =>{
	      this.overlay=false;
	    });
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
        this.$set(this.items, this.editedIndex, this.editedItem);
        } else {
          this.items.unshift(this.editedItem)
        }
        this.overlay = true;
	    var myform = new FormData();
	    myform.append("user",JSON.stringify(this.editedItem));
	    axios.post('/UpdateUser', myform).then(() =>{
	      this.overlay=false;
	    });
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
        return this.editedIndex === -1 ? 'New User' : 'Edit User'
      },
  },
  data() {
    return {
    dialog: false,
    dialogDelete: false,
    editedIndex: -1,
    editedItem: {'Username': '', 'Password': '', 'isAdmin': false, 'Email': ''},
    defaultItem: {'Username': '', 'Password': '', 'isAdmin': false, 'Email': ''},
      overlay: false,
      items:[],
      headers: [{text:'Username', value: 'Username'},{text: "Password", value: "Password"},{text: "isAdmin", value: "isAdmin"},{text: "Email", value: "Email"}, { text: 'Actions', value: 'actions', sortable: false }]
    }},
   mounted(){
     this.getUsers();
   }
  
}
</script>
