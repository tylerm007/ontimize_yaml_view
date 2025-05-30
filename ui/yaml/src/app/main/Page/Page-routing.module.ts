import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { PageHomeComponent } from './home/Page-home.component';
import { PageNewComponent } from './new/Page-new.component';
import { PageDetailComponent } from './detail/Page-detail.component';

const routes: Routes = [
  {path: '', component: PageHomeComponent},
  { path: 'new', component: PageNewComponent },
  { path: ':id', component: PageDetailComponent,
    data: {
      oPermission: {
        permissionId: 'Page-detail-permissions'
      }
    }
  },{
    path: ':page_id/PageProperty', loadChildren: () => import('../PageProperty/PageProperty.module').then(m => m.PagePropertyModule),
    data: {
        oPermission: {
            permissionId: 'PageProperty-detail-permissions'
        }
    }
}
];

export const PAGE_MODULE_DECLARATIONS = [
    PageHomeComponent,
    PageNewComponent,
    PageDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class PageRoutingModule { }