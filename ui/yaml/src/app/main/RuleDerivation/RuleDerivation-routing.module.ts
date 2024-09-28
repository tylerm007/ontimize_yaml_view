import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { RuleDerivationHomeComponent } from './home/RuleDerivation-home.component';
import { RuleDerivationNewComponent } from './new/RuleDerivation-new.component';
import { RuleDerivationDetailComponent } from './detail/RuleDerivation-detail.component';

const routes: Routes = [
  {path: '', component: RuleDerivationHomeComponent},
  { path: 'new', component: RuleDerivationNewComponent },
  { path: ':id', component: RuleDerivationDetailComponent,
    data: {
      oPermission: {
        permissionId: 'RuleDerivation-detail-permissions'
      }
    }
  }
];

export const RULEDERIVATION_MODULE_DECLARATIONS = [
    RuleDerivationHomeComponent,
    RuleDerivationNewComponent,
    RuleDerivationDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class RuleDerivationRoutingModule { }