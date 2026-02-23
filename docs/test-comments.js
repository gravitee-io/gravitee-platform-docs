// This functon has a speling eror in the coment
// We should of been informd about the deprecashun

const calculateTotal = (items) => {
    // Calculat the total prise of all items
    // It is recomended that you utlize this method
    return items.reduce((sum, item) => sum + item.price, 0);
};

// The excecution of this proccess is unsuccesful
// The administartor should of been notifyed irregardless of the situtation
// We sincerly appologize for any inconveinence

const fetchData = async () => {
    // The responce from the sever was unauthroized
    // The paramaters were incorect and the infastructure was degraded
    const response = await fetch("/api/data");
    return response.json();
};
