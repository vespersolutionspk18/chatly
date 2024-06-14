import React from 'react'

const DateItem = ({ date }) => {
    return (
        <div className='chatly-date-separator'>
            <div className='chatly-date-separator-line'>

            </div>
            <div className='chatly-date-separator-text'>
                {moment(date, frappe.defaultDatetimeFormat).format('Do MMMM YYYY')}
            </div>
            <div className='chatly-date-separator-line'></div>
        </div>
    )
}

export default DateItem