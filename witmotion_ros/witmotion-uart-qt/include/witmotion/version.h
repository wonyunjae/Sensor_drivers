namespace witmotion
{

static const std::string library_version()
{
    return "1.3.1";
}

}

#include <QtGlobal>
#if QT_VERSION < QT_VERSION_CHECK(5, 14, 0)
    #define ENDL endl
    #define HEX hex
    #define DEC dec
#else
    #define ENDL Qt::endl
    #define HEX Qt::hex
    #define DEC Qt::dec
#endif
