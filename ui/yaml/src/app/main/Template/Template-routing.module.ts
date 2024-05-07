import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { TemplateHomeComponent } from './home/Template-home.component';
import { TemplateNewComponent } from './new/Template-new.component';
import { TemplateDetailComponent } from './detail/Template-detail.component';
import { EntityAttrDetailComponent } from '../EntityAttr/detail/EntityAttr-detail.component';

const routes: Routes = [
  {path: '', component: TemplateHomeComponent},
  { path: 'new', component: TemplateNewComponent },
  { path: ':name', component: TemplateDetailComponent,
    data: {
      oPermission: {
        permissionId: 'Template-detail-permissions'
      }
    }
  },
  { path: ':entity_name/:attr', component: EntityAttrDetailComponent}
];

export const TEMPLATE_MODULE_DECLARATIONS = [
    TemplateHomeComponent,
    TemplateNewComponent,
    TemplateDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class TemplateRoutingModule { }