
export interface ChatlyPollVote{
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
	/**	User : Link - Chatly User	*/
	user_id: string
	/**	Poll : Link - Chatly Poll	*/
	poll_id: string
	/**	Option : Data	*/
	option: string
}