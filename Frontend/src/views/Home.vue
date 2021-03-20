<template>
  <div class="home">
  <div id="header" style="padding-bottom:10px">
 
  <v-text-field label="Title" v-model="title" style="display: inline-block"></v-text-field>
  <v-select v-model="selectedFormats" multiple :items="formats" label="Format" style="display: inline-block" > 
  <template v-slot:selection="data">
    {{ selectedFormats.length == formats.length ? (data.index == 0 ? '(Select All)' : '') : ( (data.index == selectedFormats.length - 1) ? data.item : (data.item+',')) }}
  </template>
  <template v-slot:prepend-item >
        <v-list-item
          ripple
          @click="toggleFormats"
        >
          <v-list-item-action class="primary theme--light"
        style="background-color: #FFFFFF;">
            <v-icon class="primary theme--light"
        style="background-color: #FFFFFF!important;">
              {{formatIcon}}
            </v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>
              (Select All)
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-divider class="mt-2"></v-divider>
      </template>
  </v-select>
  <v-select v-model="selectedAuthors" multiple :items="authors" label="Author" style="display: inline-block" >
  <template v-slot:selection="data">
    {{ selectedAuthors.length == authors.length ? (data.index == 0 ? '(Select All)' : '') : ( (data.index == selectedAuthors.length - 1) ? data.item : (data.item+',')) }}
  </template>
  <template v-slot:prepend-item >
        <v-list-item
          ripple
          @click="toggleAuthors"
        >
          <v-list-item-action class="primary theme--light"
        style="background-color: #FFFFFF;">
            <v-icon class="primary theme--light"
        style="background-color: #FFFFFF!important;">
              {{authorIcon}}
            </v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>
              (Select All)
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-divider class="mt-2"></v-divider>
      </template>
  </v-select>
  <v-select v-model="selectedPublications" multiple :items="publications" label="Publication" style="display: inline-block" >
  <template v-slot:selection="data">
    {{ selectedPublications.length == publications.length ? (data.index == 0 ? '(Select All)' : '') : ( (data.index == selectedPublications.length - 1) ? data.item : (data.item+',')) }}
  </template>
  <template v-slot:prepend-item >
        <v-list-item
          ripple
          @click="togglePublications"
        >
          <v-list-item-action class="primary theme--light"
        style="background-color: #FFFFFF;">
            <v-icon class="primary theme--light"
        style="background-color: #FFFFFF!important;">
              {{publicationIcon}}
            </v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>
              (Select All)
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-divider class="mt-2"></v-divider>
      </template>
  </v-select>
  <v-select v-model="selectedOwners" multiple :items="owners" label="Owner" style="display: inline-block" >
  <template v-slot:selection="data">
    {{ selectedOwners.length == owners.length ? (data.index == 0 ? '(Select All)' : '') : ( (data.index == selectedOwners.length - 1) ? data.item : (data.item+',')) }}
  </template>
  <template v-slot:prepend-item >
        <v-list-item
          ripple
          @click="toggleOwners"
        >
          <v-list-item-action class="primary theme--light"
        style="background-color: #FFFFFF;">
            <v-icon class="primary theme--light"
        style="background-color: #FFFFFF!important;">
              {{ownerIcon}}
            </v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>
              (Select All)
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-divider class="mt-2"></v-divider>
      </template>
  </v-select>
  <v-select v-model="selectedCountries" multiple :items="countries" label="Country" style="display: inline-block" >
  <template v-slot:selection="data">
    {{ selectedCountries.length == countries.length ? (data.index == 0 ? '(Select All)' : '') : ( (data.index == selectedCountries.length - 1) ? data.item : (data.item+',')) }}
  </template>
  <template v-slot:prepend-item >
        <v-list-item
          ripple
          @click="toggleCountries"
        >
          <v-list-item-action class="primary theme--light"
        style="background-color: #FFFFFF;">
            <v-icon class="primary theme--light"
        style="background-color: #FFFFFF!important;">
              {{countryIcon}}
            </v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>
              (Select All)
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-divider class="mt-2"></v-divider>
      </template>
  </v-select>
  <v-select v-model="selectedStates" multiple :items="states" label="State" style="display: inline-block" >
  <template v-slot:selection="data">
    {{ selectedStates.length == states.length ? (data.index == 0 ? '(Select All)' : '') : ( (data.index == selectedStates.length - 1) ? data.item : (data.item+',')) }}
  </template>
  <template v-slot:prepend-item >
        <v-list-item
          ripple
          @click="toggleStates"
        >
          <v-list-item-action class="primary theme--light"
        style="background-color: #FFFFFF;">
            <v-icon class="primary theme--light"
        style="background-color: #FFFFFF!important;">
              {{stateIcon}}
            </v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>
              (Select All)
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-divider class="mt-2"></v-divider>
      </template>
  </v-select>
  <v-select v-model="selectedCities" multiple :items="cities" label="City/Town" style="display: inline-block" >
  <template v-slot:selection="data">
    {{ selectedCities.length == cities.length ? (data.index == 0 ? '(Select All)' : '') : ( (data.index == selectedCities.length - 1) ? data.item : (data.item+',')) }}
  </template>
  <template v-slot:prepend-item >
        <v-list-item
          ripple
          @click="toggleCities"
        >
          <v-list-item-action class="primary theme--light"
        style="background-color: #FFFFFF;">
            <v-icon class="primary theme--light"
        style="background-color: #FFFFFF!important;">
              {{cityIcon}}
            </v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>
              (Select All)
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-divider class="mt-2"></v-divider>
      </template>
  </v-select>
  <v-menu
        ref="SingleDateMenu"
        v-model="SingleDateMenu"
        :close-on-content-click="false"
        :return-value.sync="SingleDate"
        transition="scale-transition"
        offset-y
        min-width="auto"
      >
        <template v-slot:activator="{ on, attrs }">
          <v-text-field style="display: inline-block"
            v-model="SingleDate"
            label="Single Date"
            prepend-icon="mdi-calendar"
            readonly
            v-bind="attrs"
            v-on="on"
          ></v-text-field>
        </template>
        <v-date-picker
          v-model="SingleDate"
          no-title
          scrollable
        >
          <v-spacer></v-spacer>
          <v-btn
            text
            color="primary"
            @click="SingleDate = null; $refs.SingleDateMenu.save(SingleDate)"
          >
            Cancel
          </v-btn>
          <v-btn
            text
            color="primary"
            @click="$refs.SingleDateMenu.save(SingleDate)"
          >
            OK
          </v-btn>
        </v-date-picker>
      </v-menu>
      <v-menu
        ref="DateRangeMenu"
        v-model="DateRangeMenu"
        :close-on-content-click="false"
        :return-value.sync="DateRange"
        transition="scale-transition"
        offset-y
        min-width="auto"
      >
        <template v-slot:activator="{ on, attrs }">
          <v-text-field style="display: inline-block"
            v-model="DateRange"
            label="Date Range"
            prepend-icon="mdi-calendar"
            readonly
            v-bind="attrs"
            v-on="on"
          ></v-text-field>
        </template>
        <v-date-picker
          v-model="DateRange"
          no-title
          range
          scrollable
        >
          <v-spacer></v-spacer>
          <v-btn
            text
            color="primary"
            @click="DateRange = null; $refs.DateRangeMenu.save(DateRange)"
          >
            Cancel
          </v-btn>
          <v-btn
            text
            color="primary"
            @click="$refs.DateRangeMenu.save(DateRange)"
          >
            OK
          </v-btn>
        </v-date-picker>
      </v-menu>
      <v-text-field label="Text" v-model="text" style="display: inline-block"></v-text-field>
      <v-select v-model="selectedEvents" multiple :items="events" label="Event" style="display: inline-block" >
  <template v-slot:selection="data">
    {{ selectedEvents.length == events.length ? (data.index == 0 ? '(Select All)' : '') : ( (data.index == selectedEvents.length - 1) ? data.item : (data.item+',')) }}
  </template>
  <template v-slot:prepend-item >
        <v-list-item
          ripple
          @click="toggleEvents"
        >
          <v-list-item-action class="primary theme--light"
        style="background-color: #FFFFFF;">
            <v-icon class="primary theme--light"
        style="background-color: #FFFFFF!important;">
              {{eventIcon}}
            </v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>
              (Select All)
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-divider class="mt-2"></v-divider>
      </template>
  </v-select>
  <v-select v-model="selectedSubjects" multiple :items="subjects" label="Subject" style="display: inline-block" >
  <template v-slot:selection="data">
    {{ selectedSubjects.length == subjects.length ? (data.index == 0 ? '(Select All)' : '') : ( (data.index == selectedSubjects.length - 1) ? data.item : (data.item+',')) }}
  </template>
  <template v-slot:prepend-item >
        <v-list-item
          ripple
          @click="toggleSubjects"
        >
          <v-list-item-action class="primary theme--light"
        style="background-color: #FFFFFF;">
            <v-icon class="primary theme--light"
        style="background-color: #FFFFFF!important;">
              {{subjectIcon}}
            </v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>
              (Select All)
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-divider class="mt-2"></v-divider>
      </template>
  </v-select>
   <v-btn rounded depressed @click="getData(true)">Search</v-btn>
   <v-btn rounded depressed @click="reset">Reset</v-btn>
   
   <v-btn v-if="$store.state.auth.isAdmin" rounded depressed @click="twitter">Get Lastest Tweets</v-btn>
   <v-btn v-if="$store.state.auth.isAdmin" rounded depressed @click="$router.push('/twitter')">Manage Accounts</v-btn>
   <v-btn v-if="$store.state.auth.isAdmin" rounded depressed @click="$router.push('/users')">Manage Users</v-btn>
   <v-btn rounded depressed @click="tweetshot">TweetShot</v-btn>
   <v-btn rounded depressed @click="logout">Logout</v-btn>
  <v-btn
        color="primary"
        class="text-none"
        rounded
        depressed
        :loading="isSelectingNews"
        @click="onButtonNewsClick"
      >
        <v-icon left>
          mdi-newspaper
        </v-icon>
        News
      </v-btn>
      <input
        ref="newsUploader"
        class="d-none"
        type="file"
        accept="doc/*"
        @change="onNewsFileChanged"
      >
  <v-btn v-if="$store.state.auth.isAdmin"
        color="primary"
        class="text-none"
        rounded
        depressed
        :loading="isSelecting"
        @click="onButtonClick"
      >
        <v-icon left>
          mdi-cloud-upload
        </v-icon>
        Import
      </v-btn>
      <input
        ref="uploader"
        class="d-none"
        type="file"
        accept="doc/*"
        @change="onFileChanged"
      >
      
      
      <v-btn
        color="primary"
        class="text-none"
        rounded
        depressed
        @click="onExport"
      >
        <v-icon left>
          mdi-cloud-download
        </v-icon>
        Export
      </v-btn>
      <v-btn v-if="$store.state.auth.isAdmin" color="red" style="color: white" rounded depressed @click="activePrompt=true">x Clear</v-btn>
   <v-btn v-if="$store.state.auth.isAdmin" color="red" style="color: white" rounded depressed @click="activePrompt2=true">x Clear Urls</v-btn>
      </div>
      <v-data-table
       dense
      	:headers="headers"
         :items="tableData"
         :options.sync="options"
         :server-items-length="totalItems"
         >
         
         </v-data-table>
         <v-dialog  v-model="activePrompt" width="500">
         Are you sure?
         <v-btn @click="cancelAlert()" style="margin-bottom: 10px;">
          Cancel
        </v-btn>
        <v-btn @click="acceptAlert()" style="margin-bottom: 10px;">
          Yes
        </v-btn>
         </v-dialog>
         <v-dialog  v-model="activePrompt2" width="500">
         Are you sure?
         <v-btn @click="cancelAlert2()" style="margin-bottom: 10px;">
          Cancel
        </v-btn>
        <v-btn @click="acceptAlert2()" style="margin-bottom: 10px;">
          Yes
        </v-btn>
         </v-dialog>
         <v-overlay :value="overlay"><v-progress-circular v-if="overlay"
      indeterminate
    ></v-progress-circular>
    <div><v-btn @click="cancelLoad()" style="margin-top:10px;">Cancel</v-btn></div>
    </v-overlay>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  name: 'Home',
  methods:{
  cancelLoad(){
     this.overlay=false;
  },
  onFileChanged(e){
  var formData = new FormData();
  formData.append("doc", e.target.files[0]);
  this.overlay=true;
  axios.post("Import",formData, {headers: {'Content-Type': 'multipart/form-data'}}).then((response) =>
  { 
  this.tableData = response.data.data;
        this.totalItems = response.data.total;
        this.formats = response.data.formats;
        this.authors = response.data.authors;
        this.publications = response.data.publications;
        this.owners = response.data.owners;
        this.countries = response.data.countries;
        this.states = response.data.states;
        this.cities = response.data.cities;
        this.events = response.data.events;
        this.subjects = response.data.subjects;
        this.overlay = false;
  }
  );
    
  },
  onNewsFileChanged(e){
  var formData = new FormData();
  formData.append("doc", e.target.files[0]);
  this.overlay=true;
  axios.post("News",formData, {headers: {'Content-Type': 'multipart/form-data'}, responseType: 'blob'}).then((response) =>
  { 
        const url = window.URL.createObjectURL(new Blob([response.data]));
		   const link = document.createElement('a');
		   link.href = url;
		   link.setAttribute('download', 'news.zip'); 
		   document.body.appendChild(link);
		   link.click();
        this.overlay = false;
  }
  );
    
  },
  tweetshot(){
    this.getData(false, false, true);
  },
  onExport(){
     this.getData(false, true);
  },
  async logout (){
        await this.$store.dispatch('LogOut')
        this.$router.push('/login')
      },
  reset(){
    this.selectedFormats = []
    this.selectedAuthors = []
    this.selectedPublications = []
    this.selectedCountries = []
    this.selectedOwners = []
    this.selectedStates = []
    this.selectedCities = []
    this.selectedEvents = []
    this.selectedSubjects = []
    this.SingleDate = null
    this.DateRange = []
    this.title = ''
    this.text = ''
  },
  twitter(){
  
  axios.post("Twitter").then((response)=>{
		console.log(response);
        });
  },
  cancelAlert(){
	this.activePrompt=false;  
  },cancelAlert2(){
	this.activePrompt2=false;  
  },acceptAlert(){
	axios.post("Clear").then((response) => {
	    this.getData(true);	
	});  
     this.activePrompt=false;
  },acceptAlert2(){
       this.overlay = true;
	axios.post("Clear2").then((response) => {
	     this.overlay = false;
	});  
     this.activePrompt2=false;
  },
    onButtonClick(){
      this.isSelecting = true
      window.addEventListener('focus', () => {
        this.isSelecting = false
      }, { once: true })
      this.$refs.uploader.click()
    
    },
    onButtonNewsClick(){
      this.isSelectingNews = true
      window.addEventListener('focus', () => {
        this.isSelectingNews = false
      }, { once: true })
      this.$refs.newsUploader.click()
    
    },
    getData(reset, doExport=false, doScreenshot=false){
        this.overlay=true
        if(reset)
           this.options.page = 1;
        const { sortBy, sortDesc, page, itemsPerPage } = this.options;
        var formData = new FormData();
        formData.append("page", page);
        formData.append("itemsPerPage", itemsPerPage);
        formData.append("title", this.title);
        formData.append("selectedFormats", this.selectedFormats);
        formData.append("selectedAuthors", this.selectedAuthors);
        formData.append("selectedPublications", this.selectedPublications);
        formData.append("selectedOwners", this.selectedOwners);
        formData.append("selectedCountries", this.selectedCountries);
        formData.append("selectedStates", this.selectedStates);
        formData.append("selectedCities", this.selectedCities);
        formData.append("selectedEvents", this.selectedEvents);
        formData.append("selectedSubjects", this.selectedSubjects);
        formData.append('SingleDate', this.SingleDate);
        formData.append('DateRange', this.DateRange);
        formData.append('text', this.text);
        formData.append('doExport', doExport);
        formData.append('doScreenshot', doScreenshot);
        if(doExport){
        axios.post("GetData", formData, {responseType: 'blob'}).then((response)=>{
        	const url = window.URL.createObjectURL(new Blob([response.data]));
		   const link = document.createElement('a');
		   link.href = url;
		   link.setAttribute('download', 'DataSet.xlsx'); 
		   document.body.appendChild(link);
		   link.click();
		   this.overlay=false;
        });
        }
        else if(doScreenshot){
        axios.post("GetData", formData, {responseType: 'blob'}).then((response)=>{
        	const url = window.URL.createObjectURL(new Blob([response.data]));
		   const link = document.createElement('a');
		   link.href = url;
		   link.setAttribute('download', 'screenshots.zip'); 
		   document.body.appendChild(link);
		   link.click();
		   this.overlay=false;
        });
        }
         else{
        axios.post("GetData", formData).then((response)=>{
		this.tableData = response.data.data;
		this.totalItems = response.data.total;
		this.formats = response.data.formats;
		this.authors = response.data.authors;
		this.publications = response.data.publications;
		this.owners = response.data.owners;
		this.countries = response.data.countries;
		this.states = response.data.states;
		this.cities = response.data.cities;
		this.events = response.data.events;
		this.subjects = response.data.subjects;
		this.overlay=false;
        }
        );
        } 
        
        
    
    },toggleFormats () {
        this.$nextTick(() => {
          if (this.selectedFormats.length == this.formats.length) {
            this.selectedFormats = []
          } else {
            this.selectedFormats = this.formats.slice()
          }
        })
      },toggleAuthors() {
        this.$nextTick(() => {
          if (this.selectedAuthors.length == this.authors.length) {
            this.selectedAuthors = []
          } else {
            this.selectedAuthors = this.authors.slice()
          }
        })
      },togglePublications() {
        this.$nextTick(() => {
          if (this.selectedPublications.length == this.publications.length) {
            this.selectedPublications = []
          } else {
            this.selectedPublications = this.publications.slice()
          }
        })
      },toggleOwners() {
        this.$nextTick(() => {
          if (this.selectedOwners.length == this.owners.length) {
            this.selectedOwners = []
          } else {
            this.selectedOwners = this.owners.slice()
          }
        })
      },toggleCountries() {
        this.$nextTick(() => {
          if (this.selectedCountries.length == this.countries.length) {
            this.selectedCountries = []
          } else {
            this.selectedCountries = this.countries.slice()
          }
        })
      },toggleStates() {
        this.$nextTick(() => {
          if (this.selectedStates.length == this.states.length) {
            this.selectedStates = []
          } else {
            this.selectedStates = this.states.slice()
          }
        })
      },toggleCities() {
        this.$nextTick(() => {
          if (this.selectedCities.length == this.cities.length) {
            this.selectedCities = []
          } else {
            this.selectedCities = this.cities.slice()
          }
        })
      },toggleEvents() {
        this.$nextTick(() => {
          if (this.selectedEvents.length == this.events.length) {
            this.selectedEvents = []
          } else {
            this.selectedEvents = this.events.slice()
          }
        })
      },toggleSubjects() {
        this.$nextTick(() => {
          if (this.selectedSubjects.length == this.subjects.length) {
            this.selectedSubjects = []
          } else {
            this.selectedSubjects = this.subjects.slice()
          }
        })
      },
  },
  components: {
    
  },
  computed:{
    formatIcon(){
      if(this.selectedFormats.length == this.formats.length)
         return 'mdi-checkbox-marked';
      return 'mdi-checkbox-blank-outline'
    },
    authorIcon(){
      if(this.selectedAuthors.length == this.authors.length)
         return 'mdi-checkbox-marked';
      return 'mdi-checkbox-blank-outline'
    },
    publicationIcon(){
      if(this.selectedPublications.length == this.publications.length)
         return 'mdi-checkbox-marked';
      return 'mdi-checkbox-blank-outline'
    },
    ownerIcon(){
      if(this.selectedOwners.length == this.owners.length)
         return 'mdi-checkbox-marked';
      return 'mdi-checkbox-blank-outline'
    },
    countryIcon(){
      if(this.selectedCountries.length == this.countries.length)
         return 'mdi-checkbox-marked';
      return 'mdi-checkbox-blank-outline'
    },
    stateIcon(){
      if(this.selectedStates.length == this.states.length)
         return 'mdi-checkbox-marked';
      return 'mdi-checkbox-blank-outline'
    },
    cityIcon(){
      if(this.selectedCities.length == this.cities.length)
         return 'mdi-checkbox-marked';
      return 'mdi-checkbox-blank-outline'
    },
    eventIcon(){
      if(this.selectedEvents.length == this.events.length)
         return 'mdi-checkbox-marked';
      return 'mdi-checkbox-blank-outline'
    },
    subjectIcon(){
      if(this.selectedSubjects.length == this.subjects.length)
         return 'mdi-checkbox-marked';
      return 'mdi-checkbox-blank-outline'
    }
  },
    watch: {
      options: {
        handler () {
          this.getData(false)
        },
        deep: true,
      },
    },
  data() {
    return {
    activePrompt: false,
    activePrompt2: false,
    selectedFormats: [],
    selectedAuthors: [],
    selectedPublications: [],
    selectedCountries: [],
    selectedOwners: [],
    selectedStates: [],
    selectedCities: [],
    selectedEvents: [],
    selectedSubjects: [],
    formats: [],
    cities: [],
    SingleDate: null,
    DateRange: [],
    DateRangeMenu: false,
    SingleDateMenu: false,
    authors: [],
    countries:[],
    publications: [],
    states: [],
    owners: [],
    events: [],
    subjects: [],
    options: {},
    totalItems: 0,
    title: '',
    text: '',
    isSelecting: false,
    isSelectingNews: false,
    overlay: false,
    headers: [{text:'Media Title', value: 'Media_Title', sortable: false},
   // {text:'Media Format', value: 'Media_Format', sortable: false},
    {text:'Media Author', value: 'Media_Author', sortable: false},
    //{text:'Media Publication_ID', value: 'Media_Publication_ID', sortable: false},
    {text:'Media Owner', value: 'Media_Owner', sortable: false},{text:'Media Country', value: 'Media_Country', sortable: false},
    //{text:'Media State', value: 'Media_State', sortable: false},
    //{text:'Media City', value:'Media_City', sortable: false},
    {text:'Media Date', value: 'Media_Date', sortable: false},{text: 'Media File', value: 'Media_File', sortable: false}, {text: 'Media Text', value: 'Media_Text', sortable: false}],
    	tableData:[]
    };
  },
  mounted(){
	//this.getData(true);  
  }
}
</script>
<style>
.v-dialog{
background: white;
}
</style>
