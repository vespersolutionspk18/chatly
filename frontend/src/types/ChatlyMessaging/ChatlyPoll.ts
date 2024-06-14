import { ChatlyPollOption } from './ChatlyPollOption'

export interface ChatlyPoll {
    creation: string
    name: string
    modified: string
    owner: string
    modified_by: string
    docstatus: 0 | 1 | 2
    parent?: string
    parentfield?: string
    parenttype?: string
    idx?: number
    /**	Question : Small Text	*/
    question: string
    /**	Options : Table - Chatly Poll Option  */
    options: ChatlyPollOption[]
    /**	Is Anonymous : Check	*/
    is_anonymous?: 0 | 1
    /**	Is Multi Choice : Check	*/
    is_multi_choice?: 0 | 1
    /**	Is Disabled : Check	*/
    is_disabled?: 0 | 1
    /**	Total Votes : Int	*/
    total_votes: number
}