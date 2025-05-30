import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { PagePropertyHomeComponent } from './home/PageProperty-home.component';
import { PagePropertyNewComponent } from './new/PageProperty-new.component';
import { PagePropertyDetailComponent } from './detail/PageProperty-detail.component';

const routes: Routes = [
  {path: '', component: PagePropertyHomeComponent},
  { path: 'new', component: PagePropertyNewComponent },
  { path: ':id', component: PagePropertyDetailComponent,
    data: {
      oPermission: {
        permissionId: 'PageProperty-detail-permissions'
      }
    }
  }
];

export const PAGEPROPERTY_MODULE_DECLARATIONS = [
    PagePropertyHomeComponent,
    PagePropertyNewComponent,
    PagePropertyDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class PagePropertyRoutingModule { }