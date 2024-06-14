
export interface ChatlyChannelMember{
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
	/**	Channel : Link - Chatly Channel	*/
	channel_id: string
	/**	User : Link - Chatly User	*/
	user_id: string
	/**	Is Admin : Check	*/
	is_admin?: 0 | 1
	/**	Last Visit : Datetime	*/
	last_visit: string
	/**	Allow notifications : Check	*/
	allow_notifications?: 0 | 1
}