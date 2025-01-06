import { Injector, ViewChild, Component, OnInit, ViewEncapsulation } from '@angular/core';
import {OTableVisibleColumnsDialogComponent, OButtonComponent, OFormComponent, OntimizeService, OListPickerComponent, OTableComponent, OColumn, OTableOptions, DialogService, SnackBarService, OSnackBarConfig} from 'ontimize-web-ngx';
import { environment } from 'src/environments/environment';
//import { OTableVisibleColumnsDialogComponent } from './visible-columns/o-table-visible-columns-dialog.component';  // This import is missing in the original file  
import { MatDialog } from '@angular/material/dialog';

@Component({
  selector: 'Entity-detail',
  templateUrl: './Entity-detail.component.html',
  styleUrls: ['./Entity-detail.component.scss']
})
export class EntityDetailComponent implements OnInit  {
  protected service: any;
  protected entity: any;
  protected dialogService: any;
  protected dialog: any
  public snackBarService: SnackBarService;
  public snackBarConfig: OSnackBarConfig;
  //protected cd: ChangeDetectorRef,
  

  @ViewChild('table', { static: true }) table: OTableComponent;

  @ViewChild('button')
  protected button: OButtonComponent;

  @ViewChild('oDetailForm') form: OFormComponent;
  
  constructor(protected injector: Injector)  {
    this.service = this.injector.get(OntimizeService);
    this.dialogService = this.injector.get(DialogService);
    this.dialog = this.injector.get(MatDialog);
    this.snackBarService = this.injector.get(SnackBarService);
    //this.table = this.injector.get(OTableComponent)
  }
  ngOnInit() {
    //this.configureService();
  }
  ngAfterViewInit() {
   // this.showHideColumns();
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
  rebuild(){
    console.log("rebuild....")
    const configuration: OSnackBarConfig = {
      action: 'Ok',
      milliseconds: 2000,
      icon: 'check_circle',
      iconPosition: 'left'
    }
    this.snackBarService.open("Please wait, Rebuilding..", configuration);
    //this.service.update({ 'name': this.data.name }, { 'download_flag': true }, "YamlFiles").subscribe((resp) => {
      this.service.query({'name': this.entity.name },
        [],
        'rebuild').subscribe((resp) => {
      console.log("rebuild: " + JSON.stringify(resp.data));
      if (resp.code === 0) {
        //this.data.downloaded = JSON.stringify(resp.data);
        //this.showDownloadInfo();
        //this.yamlFile.reload();
      } else {
        console.error(resp);
      }
    });
  }
  
  showHideColumns() {
    // TODO - get the attributes for this table and pass them to the dialog
    // columns: ColumnVisibilityConfiguration[] = [];
    // Each column should have the following properties:
    //  attr: oCol.attr,
    //  title: oCol.label,
    //  visible: oCol.visible
  
    this.service.query({'entity_name': this.entity.name },
      [],
      'getattributes').subscribe((resp) => {
        //console.log("getAttributes: " + JSON.stringify(resp.data));
        if (resp.code === 0) {
          this.showPopup(resp.data.data);
        } else {
          console.error(resp);
        }
    });
  }
  showPopup(attributes: any) {
    let columns = []
    for (let i in attributes) { 
      //console.log("Attribute: ", i, attributes[i]);
      let a =  attributes[i]
      let oCol: OColumn = new OColumn();
      oCol.attr = a.attr;
      oCol.title = a.attr;
      oCol.visible = a.exclude;
      columns.push(oCol);
    }
    //this.table.visibleColArray  = columns;
    //this.table.oTableOptions.columns = columns;
    /*
    columnVisibilityConfiguration.push(oCol);
    this.table.oTableOptions.columns = columnVisibilityConfiguration;
    this.table.visibleColumns = ["column1"];
    this.table.visibleColumns = "column1";
    this.table.columns = "column1"
    this.table.visibleColArray = ["column1"];
    console.log("Show/Hide VisibleColumns:", this.table.visibleColumns);
    console.log("Show/Hide Columns:", this.table.visibleColArray);
    console.log("Show/Hide TableOptions:", this.table.tableOptions);
    [Log] The dialog was closed (src_app_main_Entity_Entity_module_ts.js, line 265)

      columnValueFiltersToRemove: [] (0)
      columnsOrder: [] (0)
      groupColumns: undefined
      sortColumns: undefine
      visibleColArray: [] (0)
    */
    const dialogRef = this.dialog.open(OTableVisibleColumnsDialogComponent, {
      data: {
        table: this.table
      },
      maxWidth: '35vw',
      disableClose: true,
      panelClass: ['o-dialog-class', 'o-table-dialog']
    });
    // POST the new column visibility to the server and refresh the table
    dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed', result);
    });
    dialogRef.componentInstance.onAccept.subscribe((data) => {
      console.log('onAccept', data);
    });  
  }
}