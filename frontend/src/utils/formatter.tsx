export function format_date(datetime_string: string) {
    // let date = Date.parse(date_string);
    // return date.toString();
    const [date, time] = datetime_string.split('T');
    return date.toString()
}