import { Injector, ViewChild, Component, OnInit, ViewEncapsulation } from '@angular/core';
import { OButtonComponent, OFormComponent, OntimizeService, OListPickerComponent, OTableComponent} from 'ontimize-web-ngx';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'Entity-detail',
  templateUrl: './Entity-detail.component.html',
  styleUrls: ['./Entity-detail.component.scss']
})
export class EntityDetailComponent implements OnInit  {
  protected service: OntimizeService;
  protected entity: any;
  @ViewChild('table', { static: true }) table: OTableComponent;

  @ViewChild('button')
  protected button: OButtonComponent;

  @ViewChild('oDetailForm') form: OFormComponent;
  
  constructor(protected injector: Injector)  {
    this.service = this.injector.get(OntimizeService);
  }
  ngOnInit() {
    this.configureService();
   
  }

  protected configureService() {
    const conf = this.service.getDefaultServiceConfiguration();
    conf['path'] = '/Entity';
    this.service.configureService(conf);
  }
  onDataLoaded(e: object) {
    console.log(JSON.stringify(e));
    this.entity = e;
  }

  cloneEntity() {
    console.log(this.entity);
    const clone_url = environment.apiEndpoint +"/clonerow/" + this.entity["name"]; 
    console.log(clone_url);
    this.service.query({"name": this.entity["name"]},
      [],
      'clonerow').subscribe((resp) => {
        //console.log(JSON.stringify(resp));
        if (resp.code === 0) {
          console.log(JSON.stringify(resp.data));
          setTimeout(function () {}, 4000);
          console.log("Cloned Successfully");
        }
      });
  }
}