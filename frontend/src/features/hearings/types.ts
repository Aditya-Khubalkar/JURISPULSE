export type HearingStatus = 'scheduled' | 'in_progress' | 'adjourned' | 'concluded';
export interface Hearing {
  id: string;
  caseNumber: string;
  caseTitle: string;
  courtName: string;
  courtroom: string;
  judgeName: string;
  date: string;
  time: string;
  status: HearingStatus;
  purpose: string;
}
